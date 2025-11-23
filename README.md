
# cecdaemon - CEC Daemon for linux media centers

`cecdaemon` is for managing the [Consumer Electronics Control (CEC)](https://en.wikipedia.org/wiki/Consumer_Electronics_Control) capabilities of your linux media center. Some embedded systems (like Raspberry Pi) have native support for CEC. Many video cards do not have CEC capabilities, so you may need an adapter like the [one offered by PulseEight](https://www.pulse-eight.com/p/104/usb-hdmi-cec-adapter) to use CEC with your computer.

Currently it is able to translate remote buttons to computer input, run shell commands, and set the device name, and run shell scripts on standby and wake.

## Requirements:

- [python-cec](https://github.com/trainman419/python-cec/)
- [python-uinput](https://github.com/tuomasjjrasanen/python-uinput)
- [pyudev](https://github.com/pyudev/pyudev)

## Installation:
Installation should be done as root to allow installing commands to `/usr/bin/`

### Install from PIP
```
# pip3 install cecdaemon
```

### Install using setuptools
```
# python3 setup.py install
```

## Configuration
`cecdaemon` looks for a configuration file at /etc/cecdaemon.conf. The configuration file is a simple .ini style file. There are currently three main sections that can be configured:

An example configuration file is included in /usr/share/cecdaemon. To use it copy it to the /etc directory:

`cp /usr/share/cecdaemon/cecdaemon.conf-example /etc/cecdaemon.conf`

The **[tv]** section allows you to set the name that will be displayed on the tv for your device. It is truncated to the 14 character max.
```
[tv]
name = HTPC
```
The **[keymap]** section allows you to map CEC user command codes to uinput events. The remote codes can be determined using the `cecusercodes` command. The command will output the CEC User Command name, and the code in both hex and decimal. The hex code matches the CEC Specification, the decimal code is what is used in the config for readability.

```
# /usr/bin/cecusercodes
Initializing CEC, please wait...
If this takes too long ensure the device is not already in use
CEC device initialized, press remote keys or hit ^C to quit
Select pressed (hex: 0x0, dec: 0)
Up pressed (hex: 0x1, dec: 1)
Down pressed (hex: 0x2, dec: 2)
Left pressed (hex: 0x3, dec: 3)
Right pressed (hex: 0x4, dec: 4)
F1 (Blue) pressed (hex: 0x71, dec: 113)
F2 (Red) pressed (hex: 0x72, dec: 114)
F3 (Green) pressed (hex: 0x73, dec: 115)
F4 (Yellow) pressed (hex: 0x74, dec: 116)
^C
```
Keypresses can be found in [python-uinput ev.py file](https://github.com/tuomasjjrasanen/python-uinput/blob/master/src/ev.py). The format for assigning a key to a cec code looks like this:

```
[keymap]
0 = KEY_ENTER
1 = KEY_UP
#STOP
69 = KEY_X
70 = KEY_PAUSE
113 = KEY_BLUE
```
The CEC Specification states that only Select, Directions, Exit, Numbers and Function Keys get forwarded to devices, but the actual implementation varies between vendors. The `cecdaemon.conf-example` file comes with a good baseline that works well with Kodi and Steam.


The **[cmd_**_name_**]** sections can be used to run shell commands when a button is pressed or held down. For a simple press set the holdtime to 1. Use a separate section for each command. Remember to use the absolute path for the command if you are unsure what the PATH environment variable will be for the daemon. A command hook currently overrides any uinput keypresses.

```
[cmd_reboot]
# Reboots when holding the red button for 400ms
key = 114
holdtime = 4000
command = /usr/bin/systemctl reboot

[cmd_switcher]
# Open the task switcher
key = 115
holdtime = 1
command =/usr/local/scripts/switcher
```

The **[triggers]** section can be used to run shell commands when the daemon receives events such as standby or wake.
```
[triggers]
standby = /usr/bin/systemctl stop hyperiond
wake = /usr/bin/systemctl start hyperiond
```
## Usage

### Running from the command line
```
# cecdaemon --help
usage: cecdaemon [-h] [-d] [-v] [-c FILE]

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Print debug messages
  -v, --verbose         Print verbose messages
  -c FILE, --config FILE
                        Configuration file
#
```

### Using the included systemd service
Copy the script to the systemd directory:
```
# cp /usr/share/cecdaemon/cecdaemon.service-example /etc/systemd/system/cecdaemon.service
```
Reload the daemons and start the service:
`# systemctl daemon-reload`
`# systemctl start cecdaemon`

And to enable the service use:
`# systemctl enable cecdaemon`

Viewing the stderr and stdout for troubleshooting:
`# journalctl -f -u cecdaemon`
### Using in another python script
```
>>> from cecdaemon import cecdaemon
>>> cecdaemon.run()
```


## Changelog
1.0.0 - Initial beta release
