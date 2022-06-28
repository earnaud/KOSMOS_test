#!/usr/bin/python
# coding: utf-8

""" Programme principal de la camera KOSMOS
 D. Hanon 7 novembre 2020 """

from datetime import datetime
# from time import strftime
import logging

import RPi.GPIO as GPIO  # librairie pour arret propre sur boutton.

import kosmos_config as KConf
import kosmos_gps as KGps
import kosmos_csv as KCsv
import kosmos_led as KLed
import kosmos_cam as KCam
import kosmos_esc_motor as KMotor

# logging.basicConfig(level=logging.DEBUG,
#     format='%(asctime)s %(levelname)s : %(message)s',
#     datefmt='%d/%m %I:%M:%S',
#     filename='kosmos.log')
# logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s',
# datefmt='%d/%m %I:%M:%S',
# filename='kosmos.log')

logging.basicConfig(level=logging.INFO)


# Lecture du fichier de configuration
vgConf = KConf.KosmosConfig()

#Lancement LED
vgLed2 = KLed.kosmos_led(vgConf.get_val_int("SETT_LED_2"))
vgLed2.start()

# mise a jour de l'heure systeme grace au gps
vgGPS = KGps.komosGps()
vgGPS.set_date()

# date système pour les fichiers :
# ATTENTION DE NE PAS METTRE de caractères spéciaux !!
date = datetime.now()
jour = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
heure = str(date.hour) + 'h' + str(date.minute) + '-' + str(date.second)
dateStr = jour + "_" + heure

# Declaration des threads
thread_camera = KCam.KosmosCam(vgConf, dateStr)
thread_csv = KCsv.kosmosCSV(vgConf, vgGPS, dateStr)
vgLed1 = KLed.kosmos_led(vgConf.get_val_int("SETT_LED_1"))


def stop_kosmos(channel):
    """stop sur Boutton d'arret ou a la fin de la video"""
    if not thread_csv.stop:
        vgLed1.start()
        logging.info("Début de la procédure d'arrêt.")

        thread_csv.stop_thread()  # Arrêt de l'écriture du CVS
        motorThread.stop_thread()  # Arrêt routine moteur
        thread_camera.stopCam() # Arrêt routine caméra

        if thread_camera.is_alive() :
            thread_camera.join()

        # Déplacer le fichier VIDÉO sur la clef
#         if thread_camera.convert_to_mepg() is True:
#             logging.info(f"Conversion mpeg OK.")
#             if vgConf.rm_file(thread_camera.get_raw_file_name()) is True:
#                 logging.info(f"Fichier local H264 supprimé.")
#                 # on déplace le fichier converti.
#                 vgConf.moove_file(thread_camera.get_mepg_file())
#         else:
#             logging.warning(f"Problème de conversion mpeg.")
#             vgConf.moove_file(thread_camera.get_raw_file_name())
        
        # Déplacer le fichier VIDÉO sur la clef
        vgConf.moove_file(thread_camera.get_raw_file_name())

        # attendre que le csv se termine
        thread_csv.join()
        logging.info("Thread csv est terminé.")

        # Déplacer le fichier sur la clef
        vgConf.moove_file(thread_csv.get_file_name())

        motorThread.join()
        vgLed1.stop()
        vgLed1.set_on()
        logging.shutdown()
        # Commande de stop
        # os.system("sudo shutdown -h now")


# ------------------------------- MAIN----------------------------------

motorThread = KMotor.komosEscMotor(vgConf)
motorThread.arm()
motorThread.start()
thread_csv.start()
thread_camera.start()
vgLed2.stop()
vgLed2.join()
vgLed2.set_off()


# Bouton GPIO pour arret propre
GPIO.setmode(GPIO.BCM)  # on utilise les n° de GPIO et pas les broches
STOP_BUTTON_GPIO = vgConf.get_val_int("SETT_STOP_BUTTON_GPIO")
GPIO.setup(STOP_BUTTON_GPIO, GPIO.IN)
# Ajout de la fonction a executer quand on appuie sur le bouton
# (boucetime est l'entirebond pour eviter plusieurs appels)
# GPIO.RISING
GPIO.add_event_detect(STOP_BUTTON_GPIO, GPIO.FALLING,
                      callback=stop_kosmos, bouncetime=200)


# attendre que le thread camera soit termine
if thread_camera.is_alive() :
    thread_camera.join()

# si il n'a pas ete arrete par le bouton on arrete a la fin de la video
stop_kosmos(STOP_BUTTON_GPIO)

if thread_csv.is_alive():
    thread_csv.join()
if vgLed1.is_alive():
    vgLed1.join()
if vgLed2.is_alive():
    vgLed2.stop()
    vgLed2.join()
