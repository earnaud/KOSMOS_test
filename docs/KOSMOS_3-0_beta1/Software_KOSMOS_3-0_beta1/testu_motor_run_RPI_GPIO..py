#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Controle du moteur ESC
en utilisant la fonction Hard du GPIO et non pas le soft.
"""


import time
import RPi.GPIO as GPIO


def comDC(aTime: int, aFreq: int) -> float :
    """calcule le % pour avoir le temps d'impulsion aTime (en µs)"""
    vDC = round(aTime * 0.0001 * aFreq,1)
    print(f"vDC {vDC}")
    return vDC          

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)

pwm = GPIO.PWM(12, 50)  # channel=12 frequency=50Hz
pwm.start(0)
try:
    while 1:
        for vTime in range(900, 2010, 50):
            print(f"Time : {vTime} ; DC {comDC(vTime,50)}")
            pwm.ChangeDutyCycle(comDC(vTime,50))
            time.sleep(0.5)

        for vTime in range(2000, 900, -50):
            print(f"Time : {vTime} ; DC {comDC(vTime,50)}")
            pwm.ChangeDutyCycle(comDC(vTime,50))
            time.sleep(0.5)
except KeyboardInterrupt:
    pass
pwm.stop()
GPIO.cleanup()
