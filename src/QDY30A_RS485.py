from machine import Pin
import struct
import utime

from QDY30A_RS485_constants import MeasurementUnit, PrecisionLevel, BaudRate
from QDY30A_RS485_operation_constant import RS485_DE_RE, FunctionCode, RegStatus


class Logger:
    def __init__(self, enable_debug):
        self.enable_debug = enable_debug
        self.name = ''

    def debug(self, msg, *args):
        if self.enable_debug:
            print(self.name + ' DEBUG ' + msg, *args)

    def info(self, msg, *args):
        if self.enable_debug:
            print(self.name + ' INFO ' + msg, *args)

    def error(self, msg, *args):
        if self.enable_debug:
            print(self.name + ' ERROR ' + msg, *args)

    def getLogger(self, name):
        self.name = name
        return Logger(self.enable_debug)


logging = Logger(False)

logger = logging.getLogger(__name__)


class QDY30A_RS485:
    def __init__(self, uart, de_re_pin, device_addr=0x01, baudrate=9600):
        self.uart = uart
        self.de_re_pin = de_re_pin
        self.device_addr = device_addr
        self.uart_baudrate = baudrate
        self.de_re = None

    def begin(self):
        self.uart.init(baudrate=self.uart_baudrate, bits=8, parity=None, stop=1)
        self.de_re = Pin(self.de_re_pin, Pin.OUT)
        self.de_re.value(RS485_DE_RE.READ)

        self.set_local_precision_from_setting()

    def _crc16(self, data):
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return struct.pack('<H', crc)

    def crc16_modbus(self, data):
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return bytearray([crc & 0xFF, crc >> 8])

    @staticmethod
    def managed_delay(timeout):
        t = utime.ticks_ms()

        # make darn sure ticks_ms() is not about to reach max data type limit and start over
        if utime.ticks_add(t, timeout) == 0:
            t = 0

        while utime.ticks_diff(utime.ticks_ms(), t) < timeout:
            pass

    def _send_request(self, function_code, start_addr, value=None):
        # message = struct.pack('>BBH', self.device_addr, function_code,
        #                       start_addr
        #                       )
        if function_code == FunctionCode.READ:
            message = bytearray([
                self.device_addr,
                function_code,
                (start_addr >> 8) & 0xFF,  # High byte of register address
                start_addr & 0xFF,  # Low byte of register address
                0x00, 0x01  # Number of registers to read
            ])

            # message = struct.pack('>BBH',
            #                       self.device_addr,
            #                       function_code,
            #                       (start_addr >> 8) & 0xFF,  # High byte of register address
            #                       start_addr & 0xFF,  # Low byte of register address
            #                       0x00, 0x01  # Number of registers to read
            #                       )
        elif function_code == FunctionCode.WRITE and value is not None:
            message = bytearray([
                self.device_addr,
                function_code,
                (start_addr >> 8) & 0xFF,  # High byte of register address
                start_addr & 0xFF,  # Low byte of register address
                (value >> 8) & 0xFF,  # High byte of register value
                value & 0xFF  # Low byte of register value
            ])

            # message = struct.pack('>BBH',
            #                       self.device_addr,
            #                       function_code,
            #                       (start_addr >> 8) & 0xFF,  # High byte of register address
            #                       start_addr & 0xFF,  # Low byte of register address
            #                       (value >> 8) & 0xFF,  # High byte of register value
            #                       value & 0xFF  # Low byte of register value
            #                       )
        else:
            raise ValueError("Invalid function code")
        logger.debug('Sending message: %s', message)


        # if function_code == FunctionCode.WRITE and value is not None:
        #     message += struct.pack('>H', value)
        # message += self._crc16(message)
        # Calculate CRC and append it to the message
        crc = self.crc16_modbus(message)
        message += crc  # crc is already a bytearray of 2 elements

        self.de_re.value(RS485_DE_RE.WRITE)
        self.managed_delay(10)
        logger.debug('Sending message: %s', message)
        self.uart.write(message)
        self.managed_delay(10)
        self.de_re.value(RS485_DE_RE.READ)

    def _read_response(self, expected_length):
        self.managed_delay(200)
        if self.uart.any():
            response = self.uart.read(expected_length)
            if response and len(response) == expected_length:
                # Extract the CRC from the response
                received_crc = struct.unpack('<H', response[-2:])[0]
                # Calculate the CRC of the received data (excluding the CRC part of the message)
                calculated_crc = self._crc16(response[:-2])
                calculated_crc_value = struct.unpack('<H', calculated_crc)[0]
                # Verify if the calculated CRC matches the received CRC
                if received_crc == calculated_crc_value:
                    return response  # Return the response data excluding the CRC
                else:
                    logger.error("CRC check failed")
            else:
                logger.error("Invalid response length")

        return None


    def read_register(self, reg_addr):
        self._send_request(FunctionCode.READ, reg_addr)
        response = self._read_response(7)
        logger.debug('response: %s', response)
        if response:
            _, _, _, value = struct.unpack('>BBBH', response)
            return value
        return None

    def write_register(self, reg_addr, value):
        self._send_request(FunctionCode.WRITE, reg_addr, value)
        response = self._read_response(8)
        if response:
            _, _, _, value = struct.unpack('>BBBH', response)
            return value
        return None

    def set_measurement_unit(self, unit):
        if unit in MeasurementUnit.__dict__.values():
            self.write_register(RegStatus.UNITS, unit)
        else:
            raise ValueError("Invalid measurement unit")

    def set_precision(self, precision):
        if precision in PrecisionLevel.__dict__.values():
            self.write_register(RegStatus.PRECISION, precision)

    def set_baud_rate(self, baud_rate):
        """Write the baud rate of the transmitter (BaudRate.BAUD_xxx). The new speed is used by the device
        from the next power cycle: then create the UART and the object again with the new baudrate."""
        if baud_rate in BaudRate.__dict__.values():
            self.write_register(RegStatus.BAUDRATE, baud_rate)
        else:
            raise ValueError("Invalid baud rate")

    def get_baud_rate_value(self):
        return self.read_register(RegStatus.BAUDRATE)

    def get_measurement_unit_value(self):
        return self.read_register(RegStatus.UNITS)

    def get_precision_value(self):
        return self.read_register(RegStatus.PRECISION)

    def get_baud_rate_description(self):
        raw_baud = self.get_baud_rate_value()
        logger.debug('raw_baud: %s', raw_baud)
        return BaudRate.get_description(raw_baud)

    def get_measurement_unit_description(self):
        raw_unit = self.get_measurement_unit_value()
        logger.debug('raw_unit: %s', raw_unit)
        return MeasurementUnit.get_description(raw_unit)
        # return next((name for name, value in MeasurementUnit.__dict__.items() if value == raw_unit), "Unknown Unit")

    def get_measurement_unit_label(self):
        raw_unit = self.get_measurement_unit_value()
        logger.debug('raw_unit: %s', raw_unit)
        return MeasurementUnit.get_label(raw_unit)

    def get_precision_description(self):
        raw_precision = self.read_register(RegStatus.PRECISION)
        logger.debug('raw_precision: %s', raw_precision)
        return PrecisionLevel.get_description(raw_precision)

    def get_output_value(self):
        return self.read_register(RegStatus.OUTPUT)

    def get_zero_scale_value(self):
        return self.read_register(RegStatus.ZERO)

    def get_full_scale_value(self):
        return self.read_register(RegStatus.FULL)

    def get_output_value_with_precision(self, convert_to_inches=False, from_unit=MeasurementUnit.UNIT_CM):
        output_value = self.get_output_value()
        logger.debug('output_value: %s', output_value)
        precision_value = self.get_precision_value()
        logger.debug('precision_value: %s', precision_value)
        output_value_precision = output_value / (10 ** precision_value)
        if convert_to_inches:
            return self.convert_to_inches(output_value_precision, from_unit)
        else:
            return output_value_precision

    def get_zero_scale_value_with_precision(self, convert_to_inches=False, from_unit=MeasurementUnit.UNIT_CM):
        zero_scale_value = self.get_zero_scale_value()
        precision_value = self.get_precision_value()
        zero_scale_value_precision = zero_scale_value / (10 ** precision_value)
        if convert_to_inches:
            return self.convert_to_inches(zero_scale_value_precision, from_unit)
        else:
            return zero_scale_value_precision

    def get_full_scale_value_with_precision(self, convert_to_inches=False, from_unit=MeasurementUnit.UNIT_CM):
        full_scale_value = self.get_full_scale_value()
        precision_value = self.get_precision_value()
        full_scale_value_precision = full_scale_value / (10 ** precision_value)
        if convert_to_inches:
            return self.convert_to_inches(full_scale_value_precision, from_unit)
        else:
            return full_scale_value_precision

    def set_slave_address(self, new_address):
        self.write_register(RegStatus.ADDRESS, new_address)

    def get_slave_address(self):
        return self.read_register(RegStatus.ADDRESS)

    def set_local_precision_from_setting(self):
        precision = self.get_precision_value()
        self.set_local_precision(precision)

    def set_local_precision(self, precision):
        if isinstance(precision, str):
            precision_value = PrecisionLevel.__dict__.get(precision, PrecisionLevel.PRECISION_NO_DECIMAL)
        elif isinstance(precision, int):
            precision_value = precision
        else:
            raise ValueError("Invalid precision type")
        # self.write_register(RegStatus.PRECISION, precision_value)

    def convert_to_inches(self, value, from_unit=MeasurementUnit.UNIT_CM):
        """
        Convert the measurement from a specified unit to inches.

        :param value: The measurement value to convert.
        :param from_unit: The unit of the measurement value. Defaults to centimeters.
        :return: The converted value in inches.
        """
        conversion_factors = {
            MeasurementUnit.UNIT_NOT_DISPLAYED: 0,
            MeasurementUnit.UNIT_CM: 0.393701,  # 1 cm = 0.393701 inches
            MeasurementUnit.UNIT_MM: 0.0393701,  # 1 mm = 0.0393701 inches
            MeasurementUnit.UNIT_MPA: None,  # MPA is a unit of pressure, not length
            MeasurementUnit.UNIT_PA: None,  # PA is a unit of pressure, not length
            MeasurementUnit.UNIT_KPA: None,  # KPA is a unit of pressure, not length
            MeasurementUnit.UNIT_MA: None,  # MA is a unit of current, not length
        }

        if from_unit in conversion_factors and conversion_factors[from_unit] is not None:
            return value * conversion_factors[from_unit]
        else:
            print("Conversion from", from_unit, "to inches is not supported for non-length units or is unknown.")
            return None
