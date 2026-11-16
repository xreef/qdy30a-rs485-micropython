<div>
<a href="https://www.mischianti.org/forums/forum/mischiantis-libraries/qdy30a-rs485-modbus-devices/"><img
  src="https://github.com/xreef/LoRa_E32_Series_Library/raw/master/resources/buttonSupportForumEnglish.png" alt="Support forum QDY30A RS485 English"
   align="right"></a>
</div>
<div>
<a href="https://www.mischianti.org/it/forums/forum/le-librerie-di-mischianti/qdy30a-rs485-dispositivi-modbus/"><img
  src="https://github.com/xreef/LoRa_E32_Series_Library/raw/master/resources/buttonSupportForumItaliano.png" alt="Forum supporto QDY30A RS485 italiano"
  align="right"></a>
</div>

#
#
#

# MicroPython library for QDY30A RS485 Modbus level transmitters

#### Comprehensive guides and tutorials on my site www.mischianti.org

[QDY30A RS485 & MicroPython: Getting Started and Basic Usage](https://mischianti.org/qdy30a-rs485-liquid-level-micropython-esp32-pico/)

### Changelog
 - 2024-02-06 0.1.0 Initial release - Fully functional library

### Library Usage
This example demonstrates the library constructor, including the UART interface along with optional but recommended pins.

### Installation
Copy the three files of the `src` folder to the board (to the root or to `/lib`):

- `QDY30A_RS485.py`
- `QDY30A_RS485_constants.py`
- `QDY30A_RS485_operation_constant.py`

With **Thonny**: open the files, right click > *Upload to /*. With **mpremote**, from the folder of this repository:

```bash
mpremote cp src/QDY30A_RS485.py :
mpremote cp src/QDY30A_RS485_constants.py :
mpremote cp src/QDY30A_RS485_operation_constant.py :
```

### Example
This example demonstrates the library constructor, including the UART interface along with optional but recommended pins.
```python
# Initialize UART for RS485 communication on ESP32-S3
# UART 1, TX pin 17, RX pin 18, DE/RE pin 17
uart1 = UART(1, rx=Pin(18), tx=Pin(17))

qdy30a = QDY30A_RS485(uart1, de_re_pin=16)
```

Begin communication with the sensor and read the current level measurement.
```python
# Begin communication
qdy30a.begin()

# Read the current level measurement
level = qdy30a.get_output_value_with_precision()
print(f"Current Level: {level} cm")
```



