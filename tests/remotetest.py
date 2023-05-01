""" Test for the remote helper
"""
import sys
import logging
from time import sleep
import cec
from cecdaemon.remote import Remote
from cecdaemon.util import cec_init

CONF = {
    '0': 'KEY_ENTER',
    '1': 'KEY_UP',
    '2': 'KEY_DOWN',
    '3': 'KEY_LEFT',
    '4': 'KEY_RIGHT',
}

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

cec_init()

remote = Remote(cec, CONF)

while True:
    sleep(1)
