#!/usr/bin/python
# Test unitaire de lecture du fichier de config dans le repertoire courant ou sur la clef USB

import logging
from kosmos_config import *

logging.basicConfig(level=logging.DEBUG)

myConf = KosmosConfig()
myConf.print_all()

logging.info('lecture d\'une seule valeur :\n\n')
logging.info('{} = {}'.format("SETT_CSV_STEP_TIME", myConf.get_val("SETT_CSV_STEP_TIME")))
