#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Controle du moteur ESC
Utilise la lib pigpio
"""
import logging
# import os #importing os library so as to communicate with the system
import time
import RPi.GPIO as GPIO
from threading import Thread
from threading import Event

from kosmos_config import *
import subprocess


class komosEscMotor(Thread):

    def __init__(self, aConf: KosmosConfig):
        Thread.__init__(self)
        
        
        self._freq = 50 #50Hz
        self.gpio_port = aConf.get_val_int("SETT_ESC_MOTOR_PIN")

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_port, GPIO.OUT)
        self._pwm = GPIO.PWM(self.gpio_port, self._freq)  # channel=12 frequency=50Hz
        self._pwm.start(0)
        
        self.max_value = aConf.get_val_int("SETT_ESC_MOTOR_MAX_VAL")
        self.min_value = aConf.get_val_int("SETT_ESC_MOTOR_MIN_VAL")
        self.fav_value = aConf.get_val_int("SETT_ESC_MOTOR_FAVORITE_VAL")

        # temps d'attente entre deux arrêts
        self._wait_time = aConf.get_val_int("SETT_MOTOR_STOP_TIME")
        # temps de fonctionnement (à ajuster pour avoir 60°)
        self._run_time = aConf.get_val_int("SETT_MOTOR_RUN_TIME")

        # Evénement pour commander l'arrêt du Thread
        self._stopevent = Event()

    
    def compDC(self, aTime: int, aFreq: int) -> float :
        """calcule le % (duty cycle) pour avoir le temps d'impulsion aTime (en µs)"""
        logging.debug(f"Moteur DC {round(aTime * 0.0001 * aFreq,1)}.")
        return round(aTime * 0.0001 * aFreq,1) 
    
    def set_speed(self, aSpeed):
        self._pwm.ChangeDutyCycle(self.compDC(aSpeed,self._freq))
        logging.debug(f"Moteur vitesse {aSpeed}.")

    # # Procedure de calibration de l esc
    # def calibrate(self):
        # self.set_speed(0)
        # print("Déconnectez la batterie de l\'ESC et appuyez sur Enter")
        # inp = input()
        # if inp == '':
            # self.set_speed(self.max_value)
            # print("Connectez la batterie maintenant")
            # print("Vous allez entendre 2 bips, puis quand ...")
            # print("vous entendrez une tonnalité descendante, appuyez sur Entrer")
            # inp = input()
            # if inp == '':
                # self.set_speed(self.min_value)
                # print("... Tonalité spéciale")
                # time.sleep(7)
                # print("On attend toujours.")
                # time.sleep(5)
                # print("et on continue d\'attendre.")
                # self.set_speed(0)
                # time.sleep(2)
                # print("ESC prêt")
                # self.set_speed(self.min_value)
                # time.sleep(1)
                # print("Calibatrion terminée.")
            # else:
                # print("Calibratrion abandonnée.")
                # return -1
        # else:
            # print("Calibratrion abandonnée.")
            # return -1
        # logging.info('Calibatrion moteur et ESC OK.')
        # return 0

    def arm(self):
        """This is the arming procedure of an ESC"""
        #self.set_speed(self.max_value+100)
        #time.sleep(2)
        for i in range(0, 3):
            self.set_speed(self.min_value)
            time.sleep(1)
            self.set_speed(self.fav_value)
            time.sleep(1)
            self.set_speed(0)
            time.sleep(1)
        logging.info('Moteur et ESC prêts !')

    # This will stop every action your Pi is performing for ESC ofcourse.
    def arret_complet(self):
        self.set_speed(0)
        self._pwm.stop()
        logging.info('Moteur arrêt total')

    def run(self):
        """ Corps du thread; s'arrête lorque le stopevent est vrai
        https://python.developpez.com/faq/index.php?page=Thread """
        logging.info('Debut du thread moteur ESC.')

        while not self._stopevent.isSet():
            self.set_speed(0)
            logging.debug(f'Thred moteur : attente {self._wait_time} secondes.')
            self._stopevent.wait(self._wait_time)
            if not self._stopevent.isSet():
                self.set_speed(self.fav_value)
                logging.debug(f'Thred moteur : attente {self._run_time} secondes.')
                self._stopevent.wait(self._run_time)

        self.set_speed(0)
        self.arret_complet()
        logging.info('Fin du thread moteur ESC.')

    def stop_thread(self):
        """positionne l'évènement qui va provoquer l'arrêt du thread"""
        self._stopevent.set()
