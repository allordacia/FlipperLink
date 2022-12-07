import logging
import os
import subprocess
import time
from threading import Lock

import dbus

import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
from pwnagotchi.utils import StatusFile

class BTError(Exception):
    """
    Custom bluetooth exception
    """
    pass

class FlipperLink(plugins.Plugin):
    __author__ = 'Allordacia'
    __version__ = '1.0.0'
    __license__ = 'MIT'
    __description__ = 'A plugin that will add functionality for pwnagotchi to connect to the Flipper Zero'

    def __init__(self):
        # Check if the Flipper Zero is connected via bluetooth  
        self.flipper_connected = False
        self.flipper_connected = self.check_flipper()
        logging.info(self.flipper_connected)
        # Get the MAC address of the Flipper Zero provided by the user in the config file
        self.addr = self.options.get('address')

    def on_loaded(self):
        logging.info("FlipperLink plugin loaded.")

    def on_ready(self, agent):
        logging.info("FlipperLink plugin ready.")

    def on_ui_setup(self, ui):
        # Add elements to the UI
        ui.add_element('flipperlink', LabeledValue(color=BLACK, label='Flipper: ', value='Not Connected',
                                           position=(2, ui.height() - 30),
                                           label_font=fonts.Bold, text_font=fonts.Medium))

    def on_unload(self, ui):
        with ui._lock:
            ui.remove_element('flipperlink')

    def on_ui_update(self, ui):
        if self.flipper_connected:
            ui.set('flipperlink', value='Connected')
        else:
            ui.set('flipperlink', value='Not Connected')

    def check_flipper(self):
        flipper_connected = False
        addr = self.addr
        while not flipper_connected:
            flipper_connected = os.system("sudo bluetoothctl connect " + addr + "| grep -q 'Connection successful'")
            if flipper_connected == 0:
                flipper_connected = True
            else:
                flipper_connected = False
            sleep(1)

        return flipper_connected

