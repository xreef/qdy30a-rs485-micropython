from machine import UART
from QDY30A_RS485 import QDY30A_RS485, MeasurementUnit, PrecisionLevel, BaudRate
from machine import Pin

# Initialize UART for RS485 communication on ESP32-S3
# UART 1, TX pin 17, RX pin 18, DE/RE pin 17
uart1 = UART(1, rx=Pin(18), tx=Pin(17))

qdy30a = QDY30A_RS485(uart1, de_re_pin=16)

qdy30a.begin()

print("Get measurement unit {}".format(qdy30a.get_measurement_unit_description()))
print("Get precision {}".format(qdy30a.get_precision_description()))
print("Get baudrate {}".format(qdy30a.get_baud_rate_description()))
print("Get device address {}".format(hex(qdy30a.get_slave_address())))

min_level = qdy30a.get_zero_scale_value_with_precision()
max_level = qdy30a.get_full_scale_value_with_precision()
print(f"Min Level: {min_level}")
print(f"Max Level: {max_level}")

# Read the fluid level with applied precision
level = qdy30a.get_output_value_with_precision()
cm = qdy30a.get_measurement_unit_label()
print(f"Fluid Level: {level} {cm}")

# Serial output:
# Get measurement unit Centimeters
# Get precision One decimal place
# Get baudrate 9600 bps
# Get device address 0x1
# Min Level: 0.0
# Max Level: 100.0
# Fluid Level: 14.0 cm