""" Test for the trigger helper
"""
import sys
import logging
from time import sleep
import cec
from cecdaemon.trigger import Trigger

CONF = {'standby': '/usr/bin/whoami', 'wake': '/usr/bin/whoami',}
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

trigger = Trigger(cec, CONF)
cec.init()

while True:
    sleep(1)
