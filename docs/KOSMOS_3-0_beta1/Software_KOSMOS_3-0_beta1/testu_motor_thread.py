#!/usr/bin/python
# testu_motor_run
# test unitaire thread moteur avec arrêt

import time
import sys
import logging

import kosmos_esc_motor as KMotor
import kosmos_config as kConf

logging.basicConfig(level=logging.DEBUG)

#Lecture du fichier de configuration
vgConf = kConf.KosmosConfig()
moteur = KMotor.komosEscMotor(vgConf)


moteur.arm()
print ("Fin moteur arm")
#Lancement thread
moteur.start()
time.sleep(60)
moteur.stop_thread()
moteur.join()
moteur.arret_complet()

print("Fin du programme de test")
