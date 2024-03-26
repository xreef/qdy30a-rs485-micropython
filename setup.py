import sys
sys.path.pop(0)
from setuptools import setup

setup(
    name="qdy30a-rs485-micropython",
    package_dir={'': 'src'},
    py_modules=["qdy30a_rs485", "qdy30a_rs485_constants", "qdy30a_rs485_operation_constant"],
    version="0.1.0",
    description="A MicroPython library for the QDY30A RS485 level transmitter using Modbus RTU, designed for easy integration and precision measurement.",
    long_description="This library facilitates communication with the QDY30A RS485 level transmitter using the Modbus RTU protocol, simplifying the process of configuring the device and reading fluid levels. It is designed to be compatible with various MicroPython platforms including ESP32, ESP8266, STM32, and Raspberry Pi Pico.",
    keywords="RS485, Modbus, QDY30A, MicroPython, sensor, level measurement, ESP32, ESP8266, STM32, Raspberry Pi Pico",
    url="https://github.com/yourUsername/qdy30a-rs485-micropython",
    author="Renzo Mischianti",
    author_email="renzo@mischianti@gmail.com",
    maintainer="Renzo Mischianti",
    maintainer_email="renzo@mischianti@gmail.com",
    license="MIT",
    install_requires=[],
    project_urls={
        'homepage': 'https://www.mischianti.org',
        'Documentation': 'https://www.mischianti.org/category/my-libraries/qdy30a-rs485-micropython-library/',
        'Repository': 'https://github.com/yourUsername/qdy30a-rs485-micropython',
        'Bug Tracker': 'https://github.com/yourUsername/qdy30a-rs485-micropython/issues',
        'Examples': 'https://github.com/yourUsername/qdy30a-rs485-micropython/tree/main/examples',
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
