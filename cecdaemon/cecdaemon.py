""" cecdaemon: Manages CEC for a linux htpc
"""

import os
import sys
import logging
from time import sleep
from argparse import ArgumentParser
from configparser import ConfigParser
import cec

from .custom_cmd import CustomCommand
from .remote import Remote
from .tv import Tv
from .trigger import Trigger
from .util import cec_init


class CecDaemon():
    """ Creates instances of Tv, Remote, CustomCommand and Trigger
        Manages configuration parsing and command line args
    """

    def __init__(self):
        self.cec = cec
        self._parse_args()
        self._setup_logging()
        logging.info('Initializing CEC device, please wait...')
        cec_init()
        logging.info('CEC Initialized')

        conf = ConfigParser()
        if os.path.isfile(self.args.conffile):
            logging.info('Using config file %s', self.args.conffile)
            conf.read(self.args.conffile)
        else:
            logging.warning('Config file not found: %s', self.args.conffile)

        if 'tv' in conf:
            tvconf = conf['tv']
            Tv(cec, tvconf)
        else:
            Tv(cec, None)

        if 'triggers' in conf:
            triggerconf = conf['triggers']
            Trigger(cec, triggerconf)
        else:
            logging.warning(
                'No triggers section found in config, triggers disabled')

        if 'keymap' in conf:
            keymap = conf['keymap']
            remote = Remote(cec, keymap)
        else:
            remote = Remote(cec, None)

        for name in [x for x in conf.sections() if x[:4] == 'cmd_']:
            logging.debug('Creating callback for %s', name)

            try:
                cmd = conf[name]['command']
                htime = conf[name]['holdtime']
                key = conf[name]['key']

                callback = (CustomCommand(cmd, htime))
                remote.add_callback(callback.run_command, int(key))

            except AttributeError:
                logging.warning(
                    'Callback for %s not created, check format', name)

    def _setup_logging(self):
        """ Configure logging
        """
        logging.basicConfig(stream=sys.stdout, level=self.args.loglevel)

    def _parse_args(self):
        """ Parse the command line arguments
        """
        parser = ArgumentParser()
        parser.add_argument('-d', '--debug', help='Print debug messages',
                            action='store_const', dest='loglevel',
                            const=logging.DEBUG, default=logging.INFO,)

        parser.add_argument('-c', '--config', help='Configuration file',
                            metavar="FILE", dest='conffile',
                            default='/etc/cecdaemon.conf')

        self.args = parser.parse_args()

    def run(self):
        """ Keeps the instance of CecDaemon running while python-cec threads
            do callbacks
        """

        logging.info('Running...')
        while True:
            sleep(1)


def run():
    """ Run the daemon
    """
    daemon = CecDaemon()
    daemon.run()


if __name__ == "__main__":
    run()
