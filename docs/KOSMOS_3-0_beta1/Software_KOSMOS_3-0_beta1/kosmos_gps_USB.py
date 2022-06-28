#!/usr/bin/python
# -*- coding: utf-8 -*-

# Classe qui decode les trames NMEA pour en extraire les donnees importantes
# - pour mettre a jour l'heure du system grace au GPS branche en USB
# - pour prendre les positions

# David Hanon 20 octobre 2020
# Question code retour et trame RMC invalide (troiseme champs V a la place
# de A) ?


import serial  # libairie python pour liaison serie
import os  # libairie python pour lancer une commande system
import logging


class komosGps:

    def __init__(self):
        # Declaration de la liaison serie avec le capteur GPS
        # Si on veut passer sur le port série :
        # serialPort = serial.Serial("/dev/serial0", baudrate = 9600, timeout = 0.5)
        self._GpsOk = False
        try:
            self._serial_link = serial.Serial(
                port='/dev/ttyUSB0',
                baudrate=4800,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            self._GpsOk = True
            logging.info("Connexion série avec le GPS OK")
        except BaseException:
            logging.error("Problème de connexion série avec le GPS")
            
    def isOk(self) -> bool:
        """retourne l'état du GPS"""
        return self._GpsOk
    
    # mettre a jour l'heure du system grace au GPS
    def set_date(self):
        try_number = 50  # nombre de tentatives
        while try_number > 0:
            try_number = try_number - 1
            try :
                line = self._serial_link.readline().decode('ascii')
                logging.debug(f"set_date : lectures trames GPS tentatives restantes : {try_number}")
                logging.debug(line)
                if line.find("$GPRMC") != -1:  # On cherche les trames RMC
                    # on decoupe la trame entre les virgules
                    gpsData = line.split(',')
                    if (gpsData[2] == "A" or gpsData[2] == "V"):
                        # verifier si on garde pas les "V" aussi (si on a un seul satellite on a l'heure)
                        # La trame est valide
                        gpsDate = gpsData[9]  # Donnee date
                        gpsHeure = gpsData[1]  # Donnee heure
                        
                        # Mise en forme de la date Mois / jour / annee
                        sysDate = gpsDate[2:4] + '/' + gpsDate[0:2] + '/20' + gpsDate[4:6]
                        sysDate = "sudo date -s " + sysDate
                        logging.debug(sysDate)
                        # lancement de la commande system
                        ret1 = os.system(sysDate)

                        # Mise en forme de l'heure
                        gpsHeure = gpsHeure[0:2] + ':' + gpsHeure[2:4] + ':' + gpsHeure[4:6]
                        gpsHeure = "sudo date -s " + gpsHeure
                        logging.debug(gpsHeure)
                        # lancement de la commande system
                        ret2 = os.system(gpsHeure)

                        # Si tout est bon on quite
                        if (ret1 == 0 and ret2 == 0):
                            logging.info("Heure mise à jour avec le GPS")
                            return 0  # si tout est bon on retourne 0
            except UnicodeDecodeError:
                logging.warning(f"Erreur GPS : Trame passée")
                pass
        # en cas d'erreur on retourne -1
        return -1

    # Lecture et decodage des trames pour avoir la position
    # les trames $GPGGA $GPRMC et $GPGLL donnent des positions.
    def get_position(self):
        position = ""
        try_number = 10  # nombre de tentatives
        while try_number > 0:
            try_number = try_number - 1
            line = self._serial_link.readline().decode('ascii')
            # print('get_position : Lectures trames GPS tentatives
            # restantes : {}'.format(try_number))
            GP_Position = None
            
            if "$GPGGA" in line:  # On cherche les trames GGA
                # on decoupe la trame entre les virgules
                gpsData = line.split(',')
                #print("GGA : " + line)
                GP_Position = self.dec_GGA_position(gpsData)
            else:
                if "$GPGLL" in line:  # On cherche les trames GLL
                    # on decoupe la trame entre les virgules
                    gpsData = line.split(',')
                    if (gpsData[5] == "A"):
                        #print("GLL : " + line)
                        GP_Position = self.dec_GLL_position(gpsData)
                else:
                    if "$GPRMC" in line:  # On cherche les trames RMC
                        # on decoupe la trame entre les virgules
                        gpsData = line.split(',')
                        if (gpsData[2] == "A"):
                            #print("RMC : " + line)
                            GP_Position = self.dec_RMC_position(gpsData)
            if GP_Position is not None:
                logging.debug('position gps ' + self.format_position(GP_Position))
                return self.format_position(GP_Position)
        return position

    # Decodage de la trame $GPGL
    def dec_GLL_position(self, GGL_Frame):
        GGL_position = {"lat": GGL_Frame[1],
                        "NS": GGL_Frame[2],
                        "lon": GGL_Frame[3],
                        "EW": GGL_Frame[4]}
        return GGL_position

    # Decodage de la trame $GPGA
    def dec_GGA_position(self, GGA_Frame):
        GGA_position = {"lat": GGA_Frame[2],
                        "NS": GGA_Frame[3],
                        "lon": GGA_Frame[4],
                        "EW": GGA_Frame[5]}
        return GGA_position

    # Decodage de la trame $GPRMC
    def dec_RMC_position(self, RMC_Frame):
        GGA_position = {"lat": RMC_Frame[3],
                        "NS": RMC_Frame[4],
                        "lon": RMC_Frame[5],
                        "EW": RMC_Frame[6]}
        return GGA_position

    # creer une chaine en fonction du dictionnaire
    def format_position(self, dic):
        # FIXME a voir ici comment on souhaite ecrire la position.
        return dic["lat"] + ',' + dic["NS"] + ','+ dic["lon"] +','+ dic["EW"]
