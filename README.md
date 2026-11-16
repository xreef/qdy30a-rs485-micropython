# QDY30A RS485 MicroPython Library v0.1.1

![QDY30A RS485 MicroPython Logo](https://raw.githubusercontent.com/xreef/qdy30a-rs485-micropython/master/resources/QDY30A_RS485_MicroPythonLogo.png)

[![](https://img.shields.io/badge/MicroPython-library-2b2728.svg?logo=micropython)](https://micropython.org)
[![](https://img.shields.io/badge/Platform-ESP32%20%7C%20ESP8266%20%7C%20RP2040%20%7C%20STM32-green.svg)]()
[![](https://img.shields.io/badge/Protocol-Modbus%20RTU%20over%20RS485-blue.svg)]()
[![](https://img.shields.io/badge/Install-mip-orange.svg)](#-installation)
[![PyPI](https://img.shields.io/pypi/v/qdy30a-rs485-micropython.svg)](https://pypi.org/project/qdy30a-rs485-micropython/)
[![](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE.md)

A MicroPython library to read and configure the **QDY30A** submersible level transmitter over **RS485** with the
**Modbus RTU** protocol: level with the precision set on the device, zero and full scale, unit, decimals, baud rate and
slave address.

**Author:** Renzo Mischianti
**Website:** [www.mischianti.org](https://mischianti.org/category/my-libraries/qdy30a-rs485/)
**GitHub:** [xreef/qdy30a-rs485-micropython](https://github.com/xreef/qdy30a-rs485-micropython)

---

## 📚 Documentation & Tutorials

Complete tutorials on [mischianti.org](https://www.mischianti.org):

- 🌐 **[QDY30A RS485 Library Home](https://mischianti.org/category/my-libraries/qdy30a-rs485/)** - all the articles about the QDY30A libraries
- 🐍 **[QDY30A RS485 liquid level sensor with MicroPython on ESP32-S3 and Raspberry Pi Pico](https://mischianti.org/qdy30a-rs485-liquid-level-micropython-esp32-pico/)** - wiring, installation, settings and level reading
- 📖 **[QDY30A RS485 water level sensor with ESP32-S3, Arduino UNO and Raspberry Pi Pico](https://mischianti.org/qdy30a-rs485-water-level-sensor-esp32-arduino-pico/)** - the same sensor with the [Arduino library](https://github.com/xreef/QDY30A_RS485), 24V supply and transceivers explained
- 💬 🇺🇸 **[Library Forum & Support](https://mischianti.org/forums/forum/mischiantis-libraries/qdy30a-rs485-modbus-devices/)** - questions, bugs and suggestions
- 💬 🇮🇹 **[Forum e supporto alla libreria](https://mischianti.org/it/forums/forum/le-librerie-di-mischianti/qdy30a-rs485-dispositivi-modbus/)** - domande, bug e suggerimenti

---

## 📋 Table of Contents
- [Features](#-features)
- [Supported Platforms](#-supported-platforms)
- [Wiring](#-wiring)
- [Installation](#-installation)
- [Basic Usage](#-basic-usage)
- [API](#-api)
- [Included Examples](#-included-examples)
- [Changelog](#-changelog)
- [License](#-license)
- [Support & Contact](#-support--contact)

## ✨ Features

- Read the level already scaled with the precision stored in the transmitter (`get_output_value_with_precision()`)
- Optional conversion to inches (`convert_to_inches=True`)
- Read zero scale and full scale, unit, decimals, baud rate and slave address, with human readable descriptions
- Write unit, decimals, baud rate and slave address
- Direction control of the RS485 transceiver with one `DE/RE` pin
- Pure MicroPython: a `machine.UART` and a `machine.Pin`, nothing else

## 🎯 Supported Platforms

| Platform | UART | Notes |
|---|---|---|
| ESP32 / ESP32-S3 | `UART(1, rx=..., tx=...)` on any pin | Use a 3.3V transceiver (MAX3485) |
| Raspberry Pi Pico (RP2040) | `UART(1, rx=Pin(9), tx=Pin(8))` | 3.3V transceiver: the RP2040 is not 5V tolerant |
| ESP8266, STM32 | the board's UART | 3.3V transceiver |

The QDY30A needs **24V**: a step-up converter (for example an MT3608) set to 24V before you connect the probe.

## 🔌 Wiring

| Signal | ESP32-S3 | Raspberry Pi Pico | Transceiver |
|---|---|---|---|
| RX | GPIO18 | GPIO9 | RO |
| TX | GPIO17 | GPIO8 | DI |
| Direction | GPIO16 | GPIO10 | DE + RE |
| Supply | 3.3V | 3.3V | VCC |

| QDY30A wire | Connect to |
|---|---|
| Red | +24V (step-up VOUT+) |
| Green | GND (step-up VOUT-, common ground) |
| Yellow | B |
| Blue | A |

Add a 120Ω resistor across A and B at the end of the line. Diagrams and photos are in the
[tutorial](https://mischianti.org/qdy30a-rs485-liquid-level-micropython-esp32-pico/).

## 📦 Installation

### mip (recommended)
From the board's REPL, connected to the network:

```python
import mip
mip.install("github:xreef/qdy30a-rs485-micropython")
```

or from the PC with mpremote:

```bash
mpremote mip install github:xreef/qdy30a-rs485-micropython
```

### PyPI
The package is also on [PyPI](https://pypi.org/project/qdy30a-rs485-micropython/): **Thonny** installs it on the board
from *Tools > Manage packages* (search `qdy30a-rs485-micropython`). On the PC, for the IDE autocompletion:

```bash
pip install qdy30a-rs485-micropython
```

The modules use `machine` and `utime`: they run on the board, not on desktop Python.

### Manual copy
Copy the three files of the `src` folder to the board (to the root or to `/lib`): `QDY30A_RS485.py`,
`QDY30A_RS485_constants.py` and `QDY30A_RS485_operation_constant.py`. With **Thonny**: open them, right click >
*Upload to /*. With **mpremote**, from the folder of this repository:

```bash
mpremote cp src/QDY30A_RS485.py :
mpremote cp src/QDY30A_RS485_constants.py :
mpremote cp src/QDY30A_RS485_operation_constant.py :
```

## 🚀 Basic Usage

```python
from machine import UART, Pin
from QDY30A_RS485 import QDY30A_RS485, MeasurementUnit, PrecisionLevel, BaudRate

# UART 1 on GPIO18 (RX) and GPIO17 (TX), DE/RE on GPIO16 (ESP32-S3)
uart1 = UART(1, rx=Pin(18), tx=Pin(17))
qdy30a = QDY30A_RS485(uart1, de_re_pin=16)

qdy30a.begin()  # UART at 9600 baud 8N1, the default of the QDY30A

level = qdy30a.get_output_value_with_precision()
unit = qdy30a.get_measurement_unit_label()
print(f"Fluid Level: {level} {unit}")
```

The constructor accepts also `device_addr` (default `0x01`) and `baudrate` (default `9600`).

## 📖 API

| Method | Description |
|---|---|
| `begin()` | Configure the UART and the DE/RE pin, read the precision stored in the device |
| `get_output_value_with_precision(convert_to_inches=False)` | Level with the device precision applied |
| `get_zero_scale_value_with_precision()`, `get_full_scale_value_with_precision()` | Range of the transmitter |
| `get_output_value()`, `get_zero_scale_value()`, `get_full_scale_value()` | Raw register values |
| `set_measurement_unit(MeasurementUnit.UNIT_CM)` | Unit: `UNIT_NOT_DISPLAYED`, `UNIT_CM`, `UNIT_MM`, `UNIT_MPA`, `UNIT_PA`, `UNIT_KPA`, `UNIT_MA` |
| `set_precision(PrecisionLevel.PRECISION_ONE_DECIMAL)` | Decimals: `PRECISION_NO_DECIMAL` … `PRECISION_THREE_DECIMALS` |
| `set_baud_rate(BaudRate.BAUD_9600)` | Baud rate of the device (`BAUD_1200` … `BAUD_115200`), applied after a power cycle |
| `get_slave_address()`, `set_slave_address(addr)` | Modbus slave address |
| `get_measurement_unit_description()`, `get_measurement_unit_label()` | Unit as text (`Centimeters`) and as label (`cm`) |
| `get_precision_description()`, `get_baud_rate_description()` | Precision and baud rate as text |
| `read_register(reg)`, `write_register(reg, value)` | Raw Modbus register access |

## 🧪 Included Examples

| Example | What it does |
|---|---|
| `examples/get_info_and_data.py` | Reads the configuration and the level |
| `examples/set_settings.py` | Writes the unit (and, commented, precision, baud rate and address) |

## 📝 Changelog

- **2026-11-16 v0.1.1**: `set_baud_rate()`; `package.json` for installation with `mip`; examples fixed
  (`MeasurementUnit.UNIT_CM`, DE/RE comment); README with documentation, wiring and API; `setup.py`/`setup.cfg`
  module names and links fixed; published on PyPI.
- **2024-02-06 v0.1.0**: initial release.

## 📄 License

MIT License, see [LICENSE.md](LICENSE.md).

## 🤝 Support & Contact

- 🌐 Website: [www.mischianti.org](https://www.mischianti.org)
- 💬 Forum: [English](https://mischianti.org/forums/forum/mischiantis-libraries/qdy30a-rs485-modbus-devices/) · [Italiano](https://mischianti.org/it/forums/forum/le-librerie-di-mischianti/qdy30a-rs485-dispositivi-modbus/)
- 🐛 Issues: [GitHub](https://github.com/xreef/qdy30a-rs485-micropython/issues)
