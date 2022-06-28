#! /usr/bin/python
# coding: utf-8

import gpsd
import time
import logging
import os  # libairie python pour lancer une commande system
import folium

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


# Pour avoir la date en français : https://www.developpez.net/forums/d709021/autres-langages/python/general-python/date-francais/
def create_map(aPopupLab: str):
    packet = gpsd.get_current()
    myMap = folium.Map(location=[packet.lat, packet.lon])
    folium.Marker([packet.lat, packet.lon], popup=f"{aPopupLab} {time.asctime(time.localtime(time.time()))}").add_to(myMap)
    myMap.save("carte.html")
    

create_map("Kosmos allumage")





