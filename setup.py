import sys
from pathlib import Path
sys.path.pop(0)
from setuptools import setup

# PyPI page = the GitHub README (BOM removed: the file is UTF-8 with BOM)
README = (Path(__file__).parent / "README.md").read_text(encoding="utf-8-sig")

setup(
    name="qdy30a-rs485-micropython",
    package_dir={'': 'src'},
    py_modules=["QDY30A_RS485", "QDY30A_RS485_constants", "QDY30A_RS485_operation_constant"],
    version="0.1.1",
    description="A MicroPython library for the QDY30A RS485 level transmitter using Modbus RTU, designed for easy integration and precision measurement.",
    long_description=README,
    long_description_content_type="text/markdown",
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
        'Documentation': 'https://mischianti.org/category/my-libraries/qdy30a-rs485/',
        'Documentazione': 'https://mischianti.org/it/category/le-mie-librerie/qdy30a-rs485-it/',
        'Forum': 'https://mischianti.org/forums/forum/mischiantis-libraries/qdy30a-rs485-modbus-devices/',
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
