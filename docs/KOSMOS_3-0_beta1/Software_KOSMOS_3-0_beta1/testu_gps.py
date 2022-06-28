#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Programme principal de la camera KOSMOS
 D. Hanon 7 novembre 2020 """

import logging
from kosmos_gps import *

logging.basicConfig(level=logging.DEBUG)


#mise a jour de l heure systeme grace au gps
vgGps = komosGps()
vgGps.set_date()

vPos = vgGps.get_position()
logging.debug(f"Position GPS : {vPos}")