from machine import UART
from QDY30A_RS485 import QDY30A_RS485, MeasurementUnit, PrecisionLevel, BaudRate
from machine import Pin

# Initialize UART for RS485 communication on ESP32-S3
# UART 1, TX pin 17, RX pin 18, DE/RE pin 16
uart1 = UART(1, rx=Pin(18), tx=Pin(17))

qdy30a = QDY30A_RS485(uart1, de_re_pin=16)

qdy30a.begin()

qdy30a.set_measurement_unit(MeasurementUnit.UNIT_CM)
# qdy30a.set_precision(PrecisionLevel.PRECISION_ONE_DECIMAL)
# qdy30a.set_baud_rate(BaudRate.BAUD_9600)  # applied by the device after a power cycle
# qdy30a.set_slave_address(0x01)
