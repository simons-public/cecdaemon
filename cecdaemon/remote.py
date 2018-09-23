"""Remote module for cec remote control
"""

import logging
import uinput
from .const import DEFAULT_REMOTE_CONFIG
logging.getLogger(__name__)

class Remote:
    """ Takes a libcec object and a keymap and turns remote presses
        into uinput keypresses.
        Supports adding callbacks for different functions than keypresses

    :param cec: python-cec instance
    :type cec: obj
    :param keymap: cec to uinput mappings
    :type keymap: dict
    """
    def __init__(self, cec=None, keymap=None):
        self.callbacks = {}
        self.keystate = None

        if keymap is None:
            logging.warning('No keymap found in config, using default')
            self.keymap = DEFAULT_REMOTE_CONFIG
        else:
            self.keymap = keymap

        # add callback for keypresses
        cec.add_callback(self.eventrouter, cec.EVENT_KEYPRESS)

        # setup the uinput device
        devicekeys = []

        #pylint: disable=W0612
        for key, value in self.keymap.items():
            devicekeys.append(getattr(uinput, value))
        self.device = uinput.Device(devicekeys)
        logging.info('Remote initialized')

    def eventrouter(self, event, key, state):
        """ Takes a cec event and routes it to the appropriate handler

        :int event: should be 2 for keypresses
        :int key: number representing the key pressed
        :int state: 0 for down, otherwise time held before release in ms
        """
        assert event == 2

        if key in self.callbacks:
            self.callbacks[key](key, state)
        elif str(key) in self.keymap:
            self.keypress(event, key, state)
        else:
            logging.info('Key not mapped: %i', key)

    def keypress(self, event, key, state):
        """ Takes a cec remote event and outputs a keystroke

        :param event: should be 2
        :type event: int
        :param key: number representing the key pressed
        :type key: int
        :param state: 0 for down, otherwise time held before release in ms
        :type state: int
        """
        assert event == 2
        keycode = getattr(uinput, self.keymap[str(key)])

        if state == 0 and self.keystate is None:
            logging.debug('%i is mapped to %s', key, self.keymap[str(key)])
            logging.debug('Key %i down', key)
            self.keystate = "down"
            self.device.emit(keycode, 1)

        if state > 0:
            # edge case for keys that never emit state 0 (like stop)
            if self.keystate is None:
                logging.debug('Key %i down', key)
                self.device.emit(keycode, 1)

            logging.debug('Key %i up after %ims', key, state)
            self.device.emit(keycode, 0)
            self.keystate = None

    def add_callback(self, function, key):
        """ Takes a function and a key and adds a callback when that
            key is pressed

        :param function: the function to call when key is pressed
        :type function: func
        :param key: number representing the key pressed
        :type key: int
        """
        self.callbacks[key] = function
        logging.debug('Added callback')
        logging.debug(self.callbacks)
