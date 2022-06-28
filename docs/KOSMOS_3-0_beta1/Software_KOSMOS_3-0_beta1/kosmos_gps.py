#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 4 décembre 2020 :
Refonte de la classe pour utilser gpsd et la lib GPS
De cette manière le code est plus simple et il n'y a plus de problèmes
de syncho avec les trames.

Avant (20 octobre 2020)
Classe qui decode les trames NMEA pour en extraire les donnees importantes
- pour mettre a jour l'heure du system grace au GPS branche en USB
- pour prendre les positions
"""

import gpsd
import time
import os  # libairie python pour lancer une commande system
import logging


class komosGps:

    def __init__(self):
        self._GpsOk = False
        # par défaut il se connecte sur : host='127.0.0.1', port=2947
        try:
            gpsd.connect()
            self._GpsOk = True
            logging.info("Connexion GPS OK")
        except ConnectionRefusedError:
            logging.error("Problème de connexion avec le GPS")

    def isOk(self) -> bool:
        """retourne l'état du GPS"""
        return self._GpsOk

    def set_date(self) -> int:
        """mettre a jour l'heure du system grace au GPS
        retourne 0 si OK
        """
        if self._GpsOk is False:
            logging.error("Heure non mise à jour avec le GPS !")
            return -1
        try_number = 500  # nombre de tentatives
        while try_number > 0:
            try_number = try_number - 1
            try:
                logging.debug(f"Mise à jour heure depuis GPS : tentatives restantes : {try_number}")
                gpsDate = (gpsd.get_current()).time
                if gpsDate == "":
                    logging.warning("Pas de réception GPS !")
                else:
                    sysDate = "sudo date -s " + gpsDate
                    logging.debug(sysDate)
                    # lancement de la commande system
                    ret1 = os.system(sysDate)
                    if ret1 == 0:
                        logging.info("Heure mise à jour avec le GPS")
                    return 0

            except gpsd.NoFixError:
                logging.debug("GPS : FixError.")
            time.sleep(1)
        logging.error("Heure non mise à jour avec le GPS !")
        return -1

    def get_position(self) -> str:
        """Retourne la position courante"""
        if self._GpsOk is False:
            return ""
        try_number = 10  # nombre de tentatives
        position = ""
        while try_number > 0:
            try_number = try_number - 1
            try:
                packet = gpsd.get_current()
                position = packet.position()
                return position
            except gpsd.NoFixError:
                logging.debug("GPS : FixError.")
                time.sleep(1)
