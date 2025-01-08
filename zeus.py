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
# not having to reopen Autodesk Maya everytime
import importlib
import sys

if 'zeus_ui' in sys.modules:
    importlib.reload(sys.modules['zeus_ui'])
if 'zeus_model' in sys.modules:
    importlib.reload(sys.modules['zeus_model'])
if 'zeus_utils' in sys.modules:
    importlib.reload(sys.modules['zeus_utils'])

from zeus_ui import ZeusUI
from zeus_model import ZeusModel
from zeus_utils import *

global plugin_instance

class Zeus:
    def __init__(self, maya_main_window):
        self.model = ZeusModel()
        self.maya_main_window = maya_main_window
        self.ui = ZeusUI(self)
        self.ui.show()

    # Create the plugin environment
    def create_env_button_action(self):
        self.model.create_sky()
        self.model.create_cloud_bank()
        self.model.create_rain()

    def clouds_density_action(self, value):
        self.model.set_cloud_density(value)

    def clouds_density_add_keyframe_action(self):
        self.model.add_cloud_density_keyframe()

    def clouds_density_delete_keyframe_action(self):
        self.model.delete_cloud_density_keyframe()

    def clouds_storminess_add_keyframe_action(self):
        self.model.add_cloud_storminess_keyframe()

    def clouds_storminess_delete_keyframe_action(self):
        self.model.delete_cloud_storminess_keyframe()

    def clouds_storminess_action(self, is_toggled):
        self.model.set_cloud_storminess(is_toggled)

    def clouds_aod_action(self, value):
        self.model.set_cloud_details_amount(value)

    def clouds_aod_add_keyframe_action(self):
        self.model.add_cloud_details_keyframe()

    def clouds_aod_delete_keyframe_action(self):
        self.model.delete_cloud_details_keyframe()

    def rain_enabled_action(self, value):
        self.model.enable_rain(value)

    def rain_enabled_add_keyframe_action(self):
        self.model.add_rain_enabled_keyframe()

    def rain_enabled_delete_keyframe_action(self):
        self.model.delete_rain_enabled_keyframe()

    def wind_speed_action(self, value):
        self.model.set_wind_speed(value)

    def wind_speed_add_keyframe_action(self):
        self.model.add_wind_speed_keyframe()

    def wind_speed_delete_keyframe_action(self):
        self.model.delete_wind_speed_keyframe()

    def wind_direction_action(self, value, axis):
        self.model.set_wind_direction(value, axis)

    def wind_direction_add_keyframe_action(self):
        self.model.add_wind_direction_keyframe()

    def wind_direction_delete_keyframe_action(self):
        self.model.delete_wind_direction_keyframe()


# Initialize the plug-in
def initializePlugin(mobject):
    # Get Maya's window pointer
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(int(maya_main_window_ptr), QWidget)
    # Plugin instantiation
    global plugin_instance
    plugin_instance = Zeus(maya_main_window)
    om.MGlobal.displayInfo(f'[{PLUGIN_NAME}]: Plugin loaded!')


# Uninitialize the plug-in
def uninitializePlugin(mobject):
    global plugin_instance
    # Free instance memory
    if plugin_instance:
        plugin_instance.ui.close()
        plugin_instance = None
    om.MGlobal.displayInfo(f'[{PLUGIN_NAME}]: Plugin unloaded!')