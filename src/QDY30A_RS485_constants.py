class BaudRate:
    BAUD_1200 = 0
    BAUD_2400 = 1
    BAUD_4800 = 2
    BAUD_9600 = 3
    BAUD_19200 = 4
    BAUD_38400 = 5
    BAUD_57600 = 6
    BAUD_115200 = 7

    @staticmethod
    def get_description(baud_rate):
        descriptions = {
            BaudRate.BAUD_1200: "1200 bps",
            BaudRate.BAUD_2400: "2400 bps",
            BaudRate.BAUD_4800: "4800 bps",
            BaudRate.BAUD_9600: "9600 bps",
            BaudRate.BAUD_19200: "19200 bps",
            BaudRate.BAUD_38400: "38400 bps",
            BaudRate.BAUD_57600: "57600 bps",
            BaudRate.BAUD_115200: "115200 bps",
        }
        return descriptions.get(baud_rate, "Unknown Baud Rate")


class MeasurementUnit:
    UNIT_NOT_DISPLAYED = 0
    UNIT_CM = 1
    UNIT_MM = 2
    UNIT_MPA = 3
    UNIT_PA = 4
    UNIT_KPA = 5
    UNIT_MA = 6

    @staticmethod
    def get_description(unit):
        descriptions = {
            MeasurementUnit.UNIT_NOT_DISPLAYED: "Not displayed",
            MeasurementUnit.UNIT_CM: "Centimeters",
            MeasurementUnit.UNIT_MM: "Millimeters",
            MeasurementUnit.UNIT_MPA: "MegaPascals",
            MeasurementUnit.UNIT_PA: "Pascals",
            MeasurementUnit.UNIT_KPA: "KiloPascals",
            MeasurementUnit.UNIT_MA: "MilliAmps",
        }
        return descriptions.get(unit, "Unknown Measurement Unit")

    @staticmethod
    def get_label(unit):
        descriptions = {
            MeasurementUnit.UNIT_NOT_DISPLAYED: " ",
            MeasurementUnit.UNIT_CM: "cm",
            MeasurementUnit.UNIT_MM: "mm",
            MeasurementUnit.UNIT_MPA: "MPa",
            MeasurementUnit.UNIT_PA: "Pa",
            MeasurementUnit.UNIT_KPA: "kPa",
            MeasurementUnit.UNIT_MA: "mA",
        }
        return descriptions.get(unit, "Unknown")

class PrecisionLevel:
    PRECISION_NO_DECIMAL = 0
    PRECISION_ONE_DECIMAL = 1
    PRECISION_TWO_DECIMALS = 2
    PRECISION_THREE_DECIMALS = 3

    @staticmethod
    def get_description(precision):
        descriptions = {
            PrecisionLevel.PRECISION_NO_DECIMAL: "No decimal places",
            PrecisionLevel.PRECISION_ONE_DECIMAL: "One decimal place",
            PrecisionLevel.PRECISION_TWO_DECIMALS: "Two decimal places",
            PrecisionLevel.PRECISION_THREE_DECIMALS: "Three decimal places",
        }
        return descriptions.get(precision, "Unknown Precision Level")
