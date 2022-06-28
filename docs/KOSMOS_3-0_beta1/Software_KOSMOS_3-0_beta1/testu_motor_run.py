#!/usr/bin/python
# testu_motor_run
# test unitaire du moteur brushless.
# arguments temps et vitesse

import time
import sys
import logging

import kosmos_esc_motor as KMotor
import kosmos_config as kConf

logging.basicConfig(level=logging.DEBUG)

#Lecture du fichier de configuration
vgConf = kConf.KosmosConfig()
moteur = KMotor.komosEscMotor(vgConf)

if len( sys.argv ) != 3 :
    print("parametres manquants : temps (s) vitesse(%)" )
    print('vitesse comprise entre %d et %d'% (moteur.min_value, moteur.max_value))
    print("attention le moteur risque de tourner !")
    exit()

temps = int( sys.argv[1] ) #argument 1
vitesse = int( sys.argv[2] ) #argument 2
print( 'Depart pour %d secondes vitesse=%d'% (temps, vitesse))
#moteur.arm()
moteur.set_speed(vitesse)
time.sleep(temps)
moteur.set_speed(0)
#moteur.arret_complet()

print("Fin du programme de test")
