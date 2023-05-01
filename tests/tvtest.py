""" Test for tv helper
"""

import sys
import logging
from time import sleep
import cec
from cecdaemon.tv import Tv
from cecdaemon.util import cec_init

CONF = {'name': 'TESTSAT'}

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

cec_init()
television = Tv(cec, CONF)

while True:
    sleep(1)
