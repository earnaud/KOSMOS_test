#!/usr/bin/env python3
#-- coding: utf-8 --
"""
Test unitaire machine d'état
D Hanon 20 octobre 2020
""" 

import logging
import time #bibliotheque pour delay
from threading import Event
from enum import Enum, unique
import RPi.GPIO as GPIO  # librairie pour arret propre sur boutton.


import kosmos_config as KConf
import kosmos_led as KLed


logging.basicConfig(level=logging.DEBUG)

@unique
class KState(Enum):
    """Etats du kosmos"""
    STARTING = 0
    STANDBY = 1
    WORKING = 2
    STOPPING = 3
    SHUTDOWN = 4
    

class kosmos_main():
    
    def __init__(self):
        # Lecture du fichier de configuration
        self._conf = KConf.KosmosConfig()
        self.state = KState.STARTING
    
        #LEDs
        self._ledB = KLed.kosmos_led(self._conf.get_val_int("SETT_LED_B"))
        self._ledR = KLed.kosmos_led(self._conf.get_val_int("SETT_LED_R"))
        self._ledB.set_off()
        self._ledR.set_off()
        
        #évènements
        self.button_event = Event() #un ILS a été activé
        self.record_event = Event() #l'ILS start or stop record été activé
        self.stop_event = Event() #l'ILS du shutdown or stop record été activé
        
        # Boutons
        self.STOP_BUTTON_GPIO = self._conf.get_val_int("SETT_STOP_BUTTON_GPIO")
        self.RECORD_BUTTON_GPIO = self._conf.get_val_int("SETT_RECORD_BUTTON_GPIO")
        GPIO.setmode(GPIO.BCM)  # on utilise les n° de GPIO et pas les broches
        GPIO.setup(self.STOP_BUTTON_GPIO, GPIO.IN)
        GPIO.setup(self.RECORD_BUTTON_GPIO, GPIO.IN)
      
    def clear_events(self):
        """Mise à 0 des evenements attachés aux boutons"""
        self.record_event.clear()
        self.button_event.clear()
        self.stop_event.clear()
 
    def starting(self):
        """Le kosmos est en train de démarrer"""
        logging.info("ETAT : Kosmos en train de démarrer")
        self._ledB.start()
        time.sleep(5)
        self._ledB.pause()
        myMain.state = KState.STANDBY
        
    def standby(self):
        """Le kosmos est en attente du lancement de l'enregistrement"""
        logging.info("ETAT : Kosmos prêt")
        self._ledB.set_on()
        #Attendre l'appuie d'un bouton
        self.button_event.wait()
        if myMain.stop_event.isSet():
            #Prochain état : mise à l'arrêt
            self.state = KState.SHUTDOWN
        else:
            if myMain.record_event.isSet():
                #Prochain état : working
                self.state = KState.WORKING
        self._ledB.set_off()


    def working(self):
        """Le kosmos enregistre"""
        logging.info("ETAT : Kosmos en enregistrement")
        self._ledB.set_off()
        self.record_event.wait(3)
        
        #Prochain état : stopping
        self.state = KState.STOPPING

    def stopping(self):
        logging.info("ETAT : Kosmos termine son enregistrement")
        self._ledR.startAgain()
        time.sleep(5)
        self._ledR.pause()
        
        #Prochain état : stopping
        myMain.state = KState.STANDBY      

    def shutdown(self):
        logging.info("ETAT : Kosmos passe à l'arrêt total")
        if self._ledB.is_alive():
            self._ledB.stop()
            self._ledB.set_off()
        if self._ledR.is_alive():
            self._ledR.stop()
            self._ledR.join()
        self._ledR.set_on()
        exit(0)

# Debut prog principal :
myMain = kosmos_main()    
        
def stop_cb(channel):
    """Callback du bp shutdown"""
    if not myMain.stop_event.isSet():
        logging.debug("bp shutdown pressé")
        myMain.stop_event.set()
        myMain.button_event.set()

    
def record_cb(channel):
    """Callback du bp start/stop record"""
    if not myMain.record_event.isSet():
        logging.debug("bp start/stop record pressé")
        myMain.record_event.set()
        myMain.button_event.set()


    

GPIO.add_event_detect(myMain.STOP_BUTTON_GPIO, GPIO.FALLING, callback=stop_cb, bouncetime=500)
GPIO.add_event_detect(myMain.RECORD_BUTTON_GPIO, GPIO.FALLING, callback=record_cb, bouncetime=500)


myMain.state = KState.STARTING
while True:
    if myMain.state == KState.STARTING:
        myMain.starting()
        time.sleep(1)
        myMain.clear_events()
     
    if myMain.state == KState.STANDBY:
        myMain.standby()
        time.sleep(1)
        myMain.clear_events()

    if myMain.state == KState.WORKING:
        myMain.working()
        time.sleep(1)
        myMain.clear_events()

    if myMain.state == KState.STOPPING:
        myMain.stopping()
        time.sleep(1)
        myMain.clear_events()

    if myMain.state == KState.SHUTDOWN:
        myMain.shutdown()