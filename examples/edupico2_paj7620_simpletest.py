# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2025 Noqman Muzafar for Cytron Technologies
#
# SPDX-License-Identifier: Unlicense

import board
import busio
import edupico2_paj7620
import time

i2c = busio.I2C(board.GP5, board.GP4, frequency=400_000)
sensor = edupico2_paj7620.PAJ7620(i2c)

while True:
    time.sleep(0.5)
    gesture = sensor.gesture()

    if gesture == sensor.NONE:
        print(f"no gesture({gesture})")
    if gesture & sensor.UP:
        print(f"up({gesture})")
    if gesture & sensor.DOWN:
        print(f"down({gesture})")
    if gesture & sensor.LEFT:
        print(f"left({gesture})")
    if gesture & sensor.NEAR:
        print(f"near({gesture})")
    if gesture & sensor.FAR:
        print(f"far({gesture})")
    if gesture & sensor.CW:
        print(f"cw({gesture})")
    if gesture & sensor.CCW:
        print(f"ccw({gesture})")
    if gesture & sensor.WAVE:
        print(f"wave({gesture})")
        
    print(f"Proximity : {sensor.proximity()}")
 
    print("-" * 40)