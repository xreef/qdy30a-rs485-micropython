class FunctionCode:
    READ = 0x03
    WRITE = 0x06
# Define Modbus function codes
# FUNCTION_CODE_READ = 0x03
# FUNCTION_CODE_WRITE = 0x06

class RegStatus:
    ADDRESS = 0x0000
    BAUDRATE = 0x0001
    UNITS = 0x0002
    PRECISION = 0x0003
    OUTPUT = 0x0004
    ZERO = 0x0005
    FULL = 0x0006

# Define register addresses using simple constants for brevity in this example
# REG_STATUS_ADDRESS = 0x0000
# REG_STATUS_BAUDRATE = 0x0001
# REG_STATUS_UNITS = 0x0002
# REG_STATUS_PRECISION = 0x0003
# REG_STATUS_OUTPUT = 0x0004
# REG_STATUS_ZERO = 0x0005
# REG_STATUS_FULL = 0x0006

class RS485_DE_RE:
    WRITE = 1
    READ = 0
# RS485_DE_RE_WRITE = 1
# RS485_DE_RE_READ = 0
