#!/usr/bin/env python3
#-- coding: utf-8 --
"""
Test unitaire clignotage d'une led sur le GPIO
D Hanon 20 octobre 2020
""" 

import kosmos_led as kLed 
import logging
import time #bibliotheque pour delay

logging.basicConfig(level=logging.DEBUG)

led1 = kLed.kosmos_led(4) #GPIO 4
led1.start()
time.sleep(5)

logging.debug("Fin test led port 4")

led2 = kLed.kosmos_led(18) #GPIO 14
led2.set_on()
time.sleep(5)
led2.set_off()
logging.debug("Fin de test led port 18")
led1.stop()


