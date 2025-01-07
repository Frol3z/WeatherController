import maya.cmds as cmds
import maya.mel as mel
import numpy as np

import importlib
import sys

if 'py2weather_utils' in sys.modules:
    importlib.reload(sys.modules['py2weather_utils'])

from py2weather_utils import *

class WeatherModel:
    def __init__(self):
        # Debug only
        # Delete group if already present in the outliner
        if cmds.objExists(GROUP_NAME):
            cmds.delete(GROUP_NAME)
            self.group = cmds.group(empty=True, name=GROUP_NAME)
        else:
            self.group = cmds.group(empty=True, name=GROUP_NAME)

    def create_sky(self):
        # Skydome
        self.skydome = cmds.createNode('transform', name='WC::SkyDome')
        skydome_light = cmds.createNode('aiSkyDomeLight', name='aiSkyDomeLight', parent=self.skydome)
        log('SkyDomeLight created successfully!')

        # Add physical sky
        physical_sky = cmds.shadingNode('aiPhysicalSky', asTexture=True, name='aiPhysicalSky')

        # Edit intensity and sky tint attributes
        cmds.setAttr(f'{physical_sky}.intensity', 3.0)
        sky_tint_color = (0.32, 0.50, 0.84)
        cmds.setAttr(f'{physical_sky}.skyTint', *sky_tint_color, type='double3')

        # Binding physical sky to the skydome
        cmds.connectAttr(f'{physical_sky}.outColor', f'{skydome_light}.color', force=True)
        log('PhysicalSky connected successfully!')

        # Put the skydome inside the plugin group
        cmds.parent(self.skydome, self.group)

    def create_cloud_bank(self):

        # Add cloud bank
        self.cloud_container = cmds.createNode('transform', name=CLOUD_OBJECT_NAME)
        self.cloud_container_shape = cmds.createNode('fluidShape', name='cloudContainerShape', parent=self.cloud_container)

        # Load preset
        mel.eval(f'applyAttrPreset "{self.cloud_container_shape}" "customClouds" 1')

        log('Clouds created successfully!')

        # Put the cloud bank inside the plugin group
        cmds.parent(self.cloud_container, self.group)

    def create_rain(self):
        # Create the emitter
        self.rain_emitter = cmds.emitter(
            pos=(0, 0, 0),  # Position of the emitter
            type="volume",  # Emitter type set to "volume"
            n="WC:RainEmitter",  # Emitter name
            r=1000,  # Rate: Number of particles emitted per second
            sro=0,  # Start rotation: No initial rotation
            nuv=0,  # No UV tiling
            cye="none",  # Cycle: No cycling
            cyi=1,  # Cycle interval
            spd=1,  # Speed: Particle speed
            srn=0,  # Start rotation noise: No noise
            nsp=1,  # Noise strength: Set to 1
            tsp=0,  # Time step: No variation
            mxd=0,  # Maximum distance
            mnd=0,  # Minimum distance
            dx=1,  # Direction X: Emitter along X-axis
            dy=0,  # Direction Y: Emitter along Y-axis
            dz=0,  # Direction Z: Emitter along Z-axis
            sp=0,  # Speed: Particle emission speed
            vsh="cube",  # Volume shape set to cube
            vof=(0, 0, 0),  # Volume offset
            vsw=360,  # Volume sweep: 360 degrees
            tsr=0.5,  # Time step rate: 0.5
            afc=1,  # Angular factor for rotation
            afx=1,  # Angular factor X
            arx=0,  # Angular factor Y
            alx=0,  # Angular factor Z
            rnd=0,  # No randomness
            drs=0,  # Drag coefficient
            ssz=0  # Size of particles set to 0 (default)
        )

        # Scale emitter
        cmds.setAttr(f'{self.rain_emitter[0]}.scaleX', 10)
        cmds.setAttr(f'{self.rain_emitter[0]}.scaleY', 0.5)
        cmds.setAttr(f'{self.rain_emitter[0]}.scaleZ', 10)
        cmds.setAttr(f'{self.rain_emitter[0]}.rate', 0)

        # Create nParticles (and nucleus solver)
        self.rain_particles = cmds.nParticle(name='WC:RainParticles')
        cmds.connectDynamic(self.rain_particles, em=self.rain_emitter)

        # Get reference to nParticle shape node
        self.rain_particles_shape = cmds.listRelatives(self.rain_particles, shapes=True)[0]

        # Get a reference to the nucleus solver
        self.nucleus_solver = cmds.listConnections(self.rain_particles, type='nucleus')[0]
        self.nucleus_solver = cmds.rename(self.nucleus_solver, 'WC:Nucleus')

        # Additional attribute to compute deltaTime for animation purposes
        cmds.addAttr(self.nucleus_solver, longName="lastFrameTime", attributeType="float", defaultValue=0.0)

        # Create an expression to link textureOrigin with nucleus.windSpeed to move clouds
        # NOTE:
        # - opposite sign to translate them correctly with the axis
        # - scaling factor of 0.01 @todo Adjust
        expression = f"""
            float $deltaTime = time - {self.nucleus_solver}.lastFrameTime;
            
            {self.cloud_container_shape}.textureOriginX += - $deltaTime * ({self.nucleus_solver}.windSpeed * {self.nucleus_solver}.windDirectionX * 0.01);
            {self.cloud_container_shape}.textureOriginY += - $deltaTime * ({self.nucleus_solver}.windSpeed * {self.nucleus_solver}.windDirectionY * 0.01);
            {self.cloud_container_shape}.textureOriginZ += - $deltaTime * ({self.nucleus_solver}.windSpeed * {self.nucleus_solver}.windDirectionZ * 0.01);
            
            {self.nucleus_solver}.lastFrameTime = time;
        """
        cmds.expression(name="WC:cloudMovementExpression", string=expression, alwaysEvaluate=True)

        # Disable rain by default
        cmds.setAttr(f'{self.rain_particles_shape}.lifespanMode', 1)  # 1 is for constant lifespan mode
        cmds.setAttr(f'{self.rain_particles_shape}.lifespan', 1.5)

        # Create and assign rain material
        # @todo Prevent creation of multiple m_Rain materials
        rain_material = cmds.shadingNode('aiStandardSurface', asShader=True, name='m_Rain')
        cmds.select(self.rain_particles)
        cmds.hyperShade(assign=rain_material)

        log('Rain emitter and nParticles created successfully!')

        # Put the rain stuff inside the plugin group
        cmds.parent(self.rain_emitter, self.group)
        cmds.parent(self.rain_particles, self.group)
        cmds.parent(self.nucleus_solver, self.group)


    def set_cloud_density(self, value):
        normalized_value = value / 100
        cmds.setAttr(f'{self.cloud_container_shape}.opacityInputBias', normalized_value * 0.6)

    def add_cloud_density_keyframe(self):
        cmds.setKeyframe(f'{self.cloud_container_shape}.opacityInputBias')

    def delete_cloud_density_keyframe(self):
        cmds.cutKey(f'{self.cloud_container_shape}.opacityInputBias')

    def set_storminess(self, is_toggled):
        if is_toggled:
            cmds.setAttr(f'{self.cloud_container_shape}.edgeDropoff', 0.5)
        else:
            cmds.setAttr(f'{self.cloud_container_shape}.edgeDropoff', 0.372)

    def add_cloud_storminess_keyframe(self):
        cmds.setKeyframe(f'{self.cloud_container_shape}.edgeDropoff')
        # Set step function to disable interpolation
        cmds.keyTangent(f'{self.cloud_container_shape}.edgeDropoff', inTangentType="step", outTangentType="step")

    def delete_cloud_storminess_keyframe(self):
        cmds.cutKey(f'{self.cloud_container_shape}.edgeDropoff')

    def set_details_amount(self, value):
        normalized_value = value / 100
        cmds.setAttr(f'{self.cloud_container_shape}.frequencyRatio', normalized_value * 3.9 + 0.1)

    def add_cloud_details_keyframe(self):
        cmds.setKeyframe(f'{self.cloud_container_shape}.frequencyRatio')

    def delete_cloud_details_keyframe(self):
        cmds.cutKey(f'{self.cloud_container_shape}.frequencyRatio')

    def enable_rain(self, is_enabled):
        if is_enabled:
            cmds.setAttr(f'{self.rain_emitter[0]}.rate', 1000)
        else:
            cmds.setAttr(f'{self.rain_emitter[0]}.rate', 0)

    def add_rain_enabled_keyframe(self):
        cmds.setKeyframe(f'{self.rain_emitter[0]}.rate')

    def delete_rain_enabled_keyframe(self):
        cmds.cutKey(f'{self.rain_emitter[0]}.rate')

    def set_wind_speed(self, value):
        cmds.setAttr(f'{self.nucleus_solver}.windSpeed', value)

    def add_wind_speed_keyframe(self):
        cmds.setKeyframe(f'{self.nucleus_solver}.windSpeed')

    def delete_wind_speed_keyframe(self):
        cmds.cutKey(f'{self.nucleus_solver}.windSpeed')

    def set_wind_direction(self, value, axis):
        # Get previous values from the nucleus
        wind_direction = cmds.getAttr(f'{self.nucleus_solver}.windDirection')[0]
        wind_direction = np.array(wind_direction)

        # Update values locally
        if axis == 'X':
            wind_direction[0] = value
        elif axis == 'Y':
            wind_direction[1] = value
        elif axis == 'Z':
            wind_direction[2] = value

        # wind_direction[1] = 0 # Projecting to the XZ plane
        wind_direction = wind_direction / np.linalg.norm(wind_direction) # Normalizing the vector

        # Update values on the nucleus
        cmds.setAttr(f'{self.nucleus_solver}.windDirectionX', wind_direction[0])
        cmds.setAttr(f'{self.nucleus_solver}.windDirectionY', wind_direction[1])
        cmds.setAttr(f'{self.nucleus_solver}.windDirectionZ', wind_direction[2])

    def add_wind_direction_keyframe(self):
        cmds.setKeyframe(f'{self.nucleus_solver}.windDirection')

    def delete_wind_direction_keyframe(self):
        cmds.cutKey(f'{self.nucleus_solver}.windDirection')