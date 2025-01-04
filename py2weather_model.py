import maya.cmds as cmds
import maya.mel as mel

class WeatherModel:
    def __init__(self):
        self.cloud_container = None
        self.cloud_container_shape = None

    def create_cloud_bank(self):
        # Add cloud bank
        self.cloud_container = cmds.createNode('transform', name='cloudContainer')
        self.cloud_container_shape = cmds.createNode('fluidShape', name='cloudContainerShape', parent=self.cloud_container)
        mel.eval(f'applyAttrPreset "{self.cloud_container_shape}" "customClouds" 1')
        print("[py2weather] Clouds created successfully!")

    def create_sky(self):
        # Add skydome light
        skydome = cmds.createNode('transform', name='aiSkyDomeLight')
        skydome_light = cmds.createNode('aiSkyDomeLight', name='aiSkyDomeLight', parent=skydome)
        print("[py2weather] SkyDomeLight created successfully!")

        # Add physical sky
        physical_sky = cmds.shadingNode('aiPhysicalSky', asTexture=True, name='aiPhysicalSky')
        cmds.setAttr(f'{physical_sky}.intensity', 3.0)
        sky_tint_color = (0.32, 0.50, 0.84)
        cmds.setAttr(f'{physical_sky}.skyTint', *sky_tint_color, type='double3')

        cmds.connectAttr(f'{physical_sky}.outColor', f'{skydome_light}.color', force=True)
        print("[py2weather] PhysicalSky connected successfully!")

    def set_cloud_density(self, value):
        normalized_value = value / 100
        # Changing opacityInputBias between 0 and 0.6
        cmds.setAttr(f'{self.cloud_container_shape}.opacityInputBias', normalized_value * 0.6)

    def set_storminess(self, is_toggled):
        if is_toggled:
            cmds.setAttr(f'{self.cloud_container_shape}.edgeDropoff', 0.5)
        else:
            cmds.setAttr(f'{self.cloud_container_shape}.edgeDropoff', 0.372)

    def set_details_amount(self, value):
        normalized_value = value / 100
        cmds.setAttr(f'{self.cloud_container_shape}.frequencyRatio', normalized_value * 3.9 + 0.1)