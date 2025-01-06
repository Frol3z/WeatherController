# Import Maya stuff
from maya import OpenMaya as om
from maya import OpenMayaUI as omui

# Import Qt
try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
except:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import *
    from shiboken6 import wrapInstance

# Manually reloading modules to prevent caching and
# not having to reopen Autodesk Maya
import importlib
import sys

if 'py2weather_ui' in sys.modules:
    importlib.reload(sys.modules['py2weather_ui'])
if 'py2weather_model' in sys.modules:
    importlib.reload(sys.modules['py2weather_model'])
if 'py2weather_utils' in sys.modules:
    importlib.reload(sys.modules['py2weather_utils'])

from py2weather_ui import WeatherUI
from py2weather_model import WeatherModel
from py2weather_utils import *

global plugin_instance

class Weather:
    def __init__(self, maya_main_window):
        self.model = WeatherModel()
        self.maya_main_window = maya_main_window
        self.ui = WeatherUI(self)
        self.ui.show()

    def create_env_button_action(self):
        self.model.create_sky()
        self.model.create_cloud_bank()
        self.model.create_rain()

    def clouds_density_action(self, value):
        self.model.set_cloud_density(value)

    def clouds_storminess_action(self, is_toggled):
        self.model.set_storminess(is_toggled)

    def clouds_aod_action(self, value):
        self.model.set_details_amount(value)

    def rain_enabled_action(self, is_enabled):
        self.model.enable_rain(is_enabled)

    def wind_speed_action(self, value):
        self.model.set_wind_speed(value)

    def wind_direction_action(self, value, axis):
        self.model.set_wind_direction(value, axis)


# Initialize the plug-in
def initializePlugin(mobject):
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(int(maya_main_window_ptr), QWidget)

    global plugin_instance
    plugin_instance = Weather(maya_main_window)
    om.MGlobal.displayInfo("[WC] Weather Controller plug-in loaded successfully.")


# Uninitialize the plug-in
def uninitializePlugin(mobject):
    global plugin_instance
    if plugin_instance:
        plugin_instance.ui.close()
        plugin_instance = None
    om.MGlobal.displayInfo("[WC] Weather Controller plug-in unloaded successfully.")