#! /usr/bin/python
# coding: utf-8

import gpsd
import time
import logging
import os  # libairie python pour lancer une commande system

logging.basicConfig(level=logging.DEBUG)
gpsd.connect()

ret1 = -1
while (ret1 !=0):
    try:
        packet = gpsd.get_current()
        #print(packet.position())
        gpsDate = packet.time
        
        sysDate = "sudo date -s " + gpsDate
        logging.debug(sysDate)
        # lancement de la commande system
        ret1 = os.system(sysDate)
        if ret1 == 0:
            logging.info("Heure mise à jour avec le GPS")

    except (gpsd.NoFixError):
        logging.warning  ("FixError.")
        time.sleep(1) 
