# Used Maya's CreatePolygonUI devkit script as starting point
from maya import cmds
from maya import mel
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

PLUGIN_NAME = '[py2weather] '

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)

# Global variable to store the UI instance
weather_instance = None

# Utilities
def lerp(value, min, max):
    return min + (value * (max - min))

class WeatherUI(QWidget):
    def __init__(self, *args, **kwargs):
        super(WeatherUI, self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.setObjectName('WeatherUI_uniqueId')
        self.setWindowTitle('Weather UI')
        self.setGeometry(50, 50, 250, 150)
        self.initUI()

    def initUI(self):
        # Create Environment button
        self.create_env_button = QPushButton('Create Environment', self)
        self.create_env_button.clicked.connect(self.create_env_button_action)

        # Clouds density slider
        self.clouds_density_layout = QHBoxLayout()
        self.clouds_density_label = QLabel(self, text='Density')
        self.clouds_density_slider = QSlider(orientation=Qt.Horizontal, minimum=0, maximum=100, value=10)
        self.clouds_density_slider.valueChanged.connect(self.clouds_density_action)
        self.clouds_density_layout.addWidget(self.clouds_density_label)
        self.clouds_density_layout.addWidget(self.clouds_density_slider)

        # Clouds storminess checkbox
        self.clouds_storminess_layout = QHBoxLayout()
        self.clouds_storminess_label = QLabel(self, text='Storminess')
        self.clouds_storminess_checkbox = QCheckBox(self)
        self.clouds_storminess_checkbox.stateChanged.connect(self.clouds_storminess_action)
        self.clouds_storminess_layout.addWidget(self.clouds_storminess_label)
        self.clouds_storminess_layout.addWidget(self.clouds_storminess_checkbox)

        # Clouds "Amount of Details" slider
        self.clouds_aod_layout = QHBoxLayout()
        self.clouds_aod_label = QLabel(self, text='Amount of Details')
        self.clouds_aod_slider = QSlider(orientation=Qt.Horizontal, minimum=0, maximum=100, value=60)
        self.clouds_aod_slider.valueChanged.connect(self.clouds_aod_action)
        self.clouds_aod_layout.addWidget(self.clouds_aod_label)
        self.clouds_aod_layout.addWidget(self.clouds_aod_slider)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.create_env_button)
        self.layout.addLayout(self.clouds_density_layout)
        self.layout.addLayout(self.clouds_storminess_layout)
        self.layout.addLayout(self.clouds_aod_layout)

    def create_env_button_action(self):
        # Add cloud bank
        cloud_container = cmds.createNode('transform', name='cloudContainer')
        self.cloud_container_shape = cmds.createNode('fluidShape', name='cloudContainerShape', parent=cloud_container)
        mel.eval(f'applyAttrPreset "{self.cloud_container_shape}" "customClouds" 1')
        print(PLUGIN_NAME, 'Cloud bank created successfully!')

        # Add skydome light
        skydome = cmds.createNode('transform', name='aiSkyDomeLight')
        skydome_light = cmds.createNode('aiSkyDomeLight', name='aiSkyDomeLight', parent=skydome)
        print(PLUGIN_NAME, 'SkyDomeLight created successfully!')

        # Add physical sky
        physical_sky = cmds.shadingNode('aiPhysicalSky', asTexture=True, name='aiPhysicalSky')
        cmds.setAttr(f'{physical_sky}.intensity', 3.0)
        sky_tint_color = (0.32, 0.50, 0.84)
        cmds.setAttr(f'{physical_sky}.skyTint', *sky_tint_color, type='double3')

        cmds.connectAttr(f'{physical_sky}.outColor', f'{skydome_light}.color', force=True)
        print(PLUGIN_NAME, 'PhysicalSky connected successfully!')

    def clouds_density_action(self, value):
        normalized_value = value / self.clouds_density_slider.maximum()
        # Changing opacityInputBias between 0 and 0.6
        cmds.setAttr(f'{self.cloud_container_shape}.opacityInputBias', lerp(normalized_value, 0, 0.6))

    def clouds_storminess_action(self, is_toggled):
        if is_toggled:
            cmds.setAttr(f'{self.cloud_container_shape}.edgeDropoff', 0.5)
        else:
            cmds.setAttr(f'{self.cloud_container_shape}.edgeDropoff', 0.372)

    def clouds_aod_action(self, value):
        normalized_value = value / self.clouds_aod_slider.maximum()
        cmds.setAttr(f'{self.cloud_container_shape}.frequencyRatio', lerp(normalized_value, 0.1, 4.0))

# Initialize the plug-in
def initializePlugin(mobject):
    global weather_instance
    weather_instance = WeatherUI()
    weather_instance.show()
    om.MGlobal.displayInfo("Weather plug-in loaded successfully.")

# Uninitialize the plug-in
def uninitializePlugin(mobject):
    global weather_instance
    if weather_instance:
        weather_instance.close()
        weather_instance = None
    om.MGlobal.displayInfo("Weather UI plug-in unloaded successfully.")