# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Radomir Dopieralski
# SPDX-FileCopyrightText: Copyright (c) 2025 Noqman Muzafar for Cytron Technologies
#
# SPDX-License-Identifier: MIT
"""
`edupico2_paj7620`
================================================================================

Circuitpython library for PAJ7620 gesture detection and proximity sensing

This library is adapted from the PAJ7620 CircuitPython driver by
Radomir Dopieralski:
https://github.com/deshipu/CircuitPython_paj7620

* Author(s): Noqman Muzafar

Implementation Notes
--------------------

**Hardware:**

* `EDU PICO 2 <https://my.cytron.io/p-edu-pico2>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

"""

# imports

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/noqman/CircuitPython_edupico2_paj7620.git"

from adafruit_bus_device.i2c_device import I2CDevice



_ADDR = (
    b"\xefAB789BFGHIJLQ^`\x80\x81\x82\x8b\x90\x95\x96\x97\x9a\x9c"
    b"\xa5\xcc\xcd\xce\xcf\xd0\xef\x02\x03\x04%'()>^egijmnrstw\xef"
    b"AB"
)
_DATA = (
    b"\x00\x00\x00\x07\x17\x06\x01-\x0f<\x00\x1e\"\x10\x10'BD\x04"
    b"\x01\x06\n\x0c\x05\x14?\x19\x19\x0b\x13d!\x01\x0f\x10\x02\x01"
    b"9\x7f\x08\xff=\x96\x97\xcd\x01,\x01\x015\x00\x01\x00\xff\x01"
)

class PAJ7620:
    """Driver class for the PAJ7620 sensor"""
    
    NONE = 0x00
    UP = 0x01
    DOWN = 0x02
    LEFT = 0x04
    RIGHT = 0x08
    NEAR = 0x10
    FAR = 0x20
    CW = 0x40
    CCW = 0x80
    WAVE = 0x100

    buf = bytearray(2)

    def __init__(self, i2c, addr=0x73):
        self.device = I2CDevice(i2c, addr)

        with self.device as device:
            for address, data in zip(_ADDR, _DATA):
                self.buf[0] = address
                self.buf[1] = data
                device.write(self.buf)

    def gesture(self):
        """Read and clear the gestures from the sensor."""

        with self.device as device:
            device.write_then_readinto(b"\x43", self.buf)
        return int.from_bytes(self.buf, "little")
    
    def proximity_raw(self):
        """ Read raw proximity value from register 0x6C (S_AvgY[8:1])."""
        
        with self.device as device:
            # write register address, then read one byte
            device.write_then_readinto(bytes([0x6C]), self.buf, in_end=1)
        return self.buf[0]

    def proximity(self):
        """Convert raw PAJ7620 proximity data into a usable 0–255 range."""
        
        raw_value = self.proximity_raw()
            
        # Map raw_value from 70-255 to 0-255; clamp values below 70 to 0 due to inconsistent output
        if raw_value < 70:
            return 0
        
        mapped_value = (255 * (raw_value - 70)) // 185
        return min(mapped_value, 255)  # Ensure output doesn't exceed 255