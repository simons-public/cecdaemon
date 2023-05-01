""" Utility functions
"""

import pyudev
import cec

def cec_init():
    """ libcec gained support for the new CEC Linux kernel subsystem. However,
        it currently doesn't use this by default. So we check for the existence
        of the device created by the new kernel module and then tell libcec
        to specifically use the new "Linux" interface.
    """

    context = pyudev.Context()
    devices = list(context.list_devices(subsystem='cec'))

    if len(devices) > 0:
        cec.init('Linux')
    else:
        cec.init()