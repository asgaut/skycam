# This is based on the following code:
# https://github.com/ralf1070/Adafruit_Python_SHT31/blob/master/Adafruit_SHT31.py
# https://github.com/ControlEverythingCommunity/SHT31/blob/master/Python/SHT31.py

# Datasheet from Sensirion for address and command information:
# https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/2_Humidity_Sensors/Sensirion_Humidity_Sensors_SHT3x_Datasheet_digital.pdf

import smbus2 as smbus
import time

# SHT31D default I2C address.
SHT31_DEFAULT_ADDR = 0x44

class Sensor:

    def __init__(self, address = SHT31_DEFAULT_ADDR, bus_number = 1):
        self._bus = smbus.SMBus(bus_number)
        self._address = address

    def read_temperature_humidity(self):
# Send measurement command, 0x2C
# High repeatability measurement, 0x06
        self._bus.write_i2c_block_data(self._address, 0x2C, [0x06])
        time.sleep(0.015)

# Read data back from 0x00, 6 bytes
# Temp MSB, Temp LSB, Temp CRC, Humididty MSB, Humidity LSB, Humidity CRC
        buffer = self._bus.read_i2c_block_data(self._address, 0x00, 6)

# Check temperature CRC
        if buffer[2] != self._crc8(buffer[0:2]):
            return (float("nan"), float("nan"))

# Check humidity CRC
        if buffer[5] != self._crc8(buffer[3:5]):
            return (float("nan"), float("nan"))

# Convert the data
        temp_C = -45 + (175 * (buffer[0] * 256 + buffer[1]) / 65535.0)
        humidity = 100 * (buffer[3] * 256 + buffer[4]) / 65535.0
        return (temp_C, humidity)

    def _crc8(self, buffer):
        """ Polynomial 0x31 (x8 + x5 + x4 +1) """
        polynomial = 0x31;
        crc = 0xFF;
        index = 0
        for index in range(0, len(buffer)):
            crc ^= buffer[index]
            for i in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ polynomial
                else:
                    crc = (crc << 1)
        return crc & 0xFF

def read_and_print():
    """Test the above code"""
    s = Sensor()
    (t, h) = s.read_temperature_humidity()
    print("temperature: {0} C, humidity: {1}".format(t, h))

if __name__ == "__main__":
    read_and_print()