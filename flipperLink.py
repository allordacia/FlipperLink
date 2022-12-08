import pwnagotchi
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.faces as faces
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.utils as utils
from pwnagotchi.ui.components import *
from pwnagotchi.ui.state import State
import logging
from time import sleep
import os

class FlipperLink(plugins.Plugin):
    __author__ = 'Allordacia'
    __version__ = '1.0.0'
    __license__ = 'MIT'
    __description__ = 'A plugin that will add functionality for pwnagotchi to connect to the Flipper Zero'

    def __init__(self):
        # Check if the Flipper Zero is connected via bluetooth  
        self.running = False

    def on_loaded(self):
        self.flipper_connected = False
        self.flipper_connected = self.check_flipper()
        logging.info(self.flipper_connected)
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
        while not flipper_connected:
            flipper_connected = os.system("sudo bluetoothctl connect " + self.options['mac'] + "| grep -q 'Connection successful'")
            if flipper_connected == 0:
                flipper_connected = True
                logging.info("flipperLink has conencted to %s" % self.options['mac'])
            else:
                flipper_connected = False
            sleep(1)

        return flipper_connected

