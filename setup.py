import sys
sys.path.pop(0)
from setuptools import setup

setup(
    name="qdy30a-rs485-micropython",
    package_dir={'': 'src'},
    py_modules=["QDY30A_RS485", "QDY30A_RS485_constants", "QDY30A_RS485_operation_constant"],
    version="0.1.1",
    description="A MicroPython library for the QDY30A RS485 level transmitter using Modbus RTU, designed for easy integration and precision measurement.",
    long_description="This library facilitates communication with the QDY30A RS485 level transmitter using the Modbus RTU protocol, simplifying the process of configuring the device and reading fluid levels. It is designed to be compatible with various MicroPython platforms including ESP32, ESP8266, STM32, and Raspberry Pi Pico.",
    keywords="RS485, Modbus, QDY30A, MicroPython, sensor, level measurement, ESP32, ESP8266, STM32, Raspberry Pi Pico",
    url="https://github.com/xreef/qdy30a-rs485-micropython",
    author="Renzo Mischianti",
    author_email="renzo.mischianti@gmail.com",
    maintainer="Renzo Mischianti",
    maintainer_email="renzo.mischianti@gmail.com",
    license="MIT",
    install_requires=[],
    project_urls={
        'homepage': 'https://www.mischianti.org',
        'Documentation': 'https://mischianti.org/qdy30a-rs485-liquid-level-micropython-esp32-pico/',
        'Repository': 'https://github.com/xreef/qdy30a-rs485-micropython',
        'Bug Tracker': 'https://github.com/xreef/qdy30a-rs485-micropython/issues',
        'Examples': 'https://github.com/xreef/qdy30a-rs485-micropython/tree/master/examples',
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: Implementation :: MicroPython",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Scientific/Engineering",
    ],
)
