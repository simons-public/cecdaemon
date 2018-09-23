"""Runs a command when a button is pressed
"""

from subprocess import Popen, PIPE, STDOUT
import logging
logging.getLogger(__name__)

class CustomCommand():
    """Runs a command based on initial configuration

    :str command: the command to run
    :str holdtime: the minimum length of time in ms
    """

    def __init__(self, command, holdtime):
        self.holdtime = holdtime
        self.command = command

    def run_command(self, key, state):
        """Runs a command if state > the config holdtime

        :str key: the key pressed
        :int state: the time key was pressed in ms
        """
        logging.info('running command: %s', self.command)
        try:
            if state >= int(self.holdtime):
                cmd = Popen(self.command.split(), stdout=PIPE, stderr=STDOUT)
                output, _ = cmd.communicate()
                logging.debug(str(output))
        except OSError:
            logging.warning('failed to run custom command for key %s', key)
