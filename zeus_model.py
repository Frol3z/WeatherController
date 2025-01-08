import maya.cmds as cmds
import maya.mel as mel
import numpy as np

import importlib
import sys

if 'zeus_utils' in sys.modules:
    importlib.reload(sys.modules['zeus_utils'])

from zeus_utils import *

class ZeusModel:
    def __init__(self):
        # If GROUP_NAME group already in the outliner
        # get the objects references
        # otherwise it will create the group
        if cmds.objExists(GROUP_NAME):
            self.set_reference_from_outliner()
        else:
            self.group = cmds.group(empty=True, name=GROUP_NAME)

    def set_reference_from_outliner(self):
        # Check for skydome
        children = cmds.ls(SKYDOME_OBJECT_NAME, long=True) or []
        if children:
            self.skydome = children[0]
            log('Found ' + self.skydome)
        else:
            log('No skydome object found!')

        # Check for clouds
        children = cmds.ls(CLOUD_OBJECT_NAME, long=True) or []
        if children:
            self.cloud_container = children[0]
            log('Found ' + self.cloud_container)
        else:
            log('No cloud object found!')

        # Check for rain emitter
        children = cmds.ls(RAIN_EMITTER_OBJECT_NAME, long=True) or []
        if children:
            self.rain_emitter = children[0]
            log('Found ' + self.rain_emitter)
        else:
            log('No rain emitter object found!')

        # Check for rain particles
        children = cmds.ls(RAIN_PARTICLES_OBJECT_NAME, long=True) or []
        if children:
            self.rain_particles = children[0]
            log('Found ' + self.rain_particles)
        else:
            log('No rain particles object found!')

        # Check for nucleus solver
        children = cmds.ls(NUCLEUS_OBJECT_NAME, long=True) or []
        if children:
            self.nucleus = children[0]
            log('Found ' + self.nucleus)
        else:
            log('No nucleus object found!')

    def create_sky(self):
        # Create skydome
        self.skydome = cmds.createNode('transform', name=SKYDOME_OBJECT_NAME)
        skydome_light = cmds.createNode('aiSkyDomeLight', name='aiSkyDomeLight', parent=self.skydome)
        log(SKYDOME_OBJECT_NAME + ' created successfully!')

        # Add physical sky
        physical_sky = cmds.shadingNode('aiPhysicalSky', asTexture=True, name='aiPhysicalSky')

        # Edit intensity and sky tint attributes
        cmds.setAttr(f'{physical_sky}.intensity', 3.0)
        sky_tint_color = (0.32, 0.50, 0.84)
        cmds.setAttr(f'{physical_sky}.skyTint', *sky_tint_color, type='double3')

        # Connect physical sky to the skydome
        cmds.connectAttr(f'{physical_sky}.outColor', f'{skydome_light}.color', force=True)
        log('aiPhysicalSky connected to ' + SKYDOME_OBJECT_NAME + ' successfully!')

        # Insert in the plugin group
        cmds.parent(self.skydome, self.group)

    def create_cloud_bank(self):
        # Create cloud fluid container
        self.cloud_container = cmds.createNode('transform', name=CLOUD_OBJECT_NAME)
        cloud_container_shape = cmds.createNode('fluidShape', name='cloudContainerShape', parent=self.cloud_container)

        # Load custom preset
        mel.eval(f'applyAttrPreset "{cloud_container_shape}" "customClouds" 1')
        log(CLOUD_OBJECT_NAME + ' created successfully!')

        # Insert in the plugin group
        cmds.parent(self.cloud_container, self.group)

    def create_rain(self):
        # Create particle emitter
        self.rain_emitter = cmds.emitter(
            pos=(0, 0, 0),  # Position of the emitter
            type="volume",  # Emitter type set to "volume"
            n=RAIN_EMITTER_OBJECT_NAME,  # Emitter name
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
        self.rain_emitter = self.rain_emitter[0]

        # Scale emitter
        cmds.setAttr(f'{self.rain_emitter}.scaleX', 10)
        cmds.setAttr(f'{self.rain_emitter}.scaleY', 0.5)
        cmds.setAttr(f'{self.rain_emitter}.scaleZ', 10)
        cmds.setAttr(f'{self.rain_emitter}.rate', 0)

        log(RAIN_EMITTER_OBJECT_NAME + ' created successfully!')

        # Create nParticles (and nucleus solver)
        self.rain_particles = cmds.nParticle(name=RAIN_PARTICLES_OBJECT_NAME)
        cmds.connectDynamic(self.rain_particles, em=self.rain_emitter)

        # Get reference to nParticle shape node
        rain_particles_shape = cmds.listRelatives(self.rain_particles, shapes=True)[0]

        # Disable rain by default
        cmds.setAttr(f'{rain_particles_shape}.lifespanMode', 1)  # 1 is for constant lifespan mode
        cmds.setAttr(f'{rain_particles_shape}.lifespan', 1.5)

        # Get a reference to the nucleus solver
        self.nucleus = cmds.listConnections(self.rain_particles, type='nucleus')[0]
        self.nucleus = cmds.rename(self.nucleus, NUCLEUS_OBJECT_NAME)

        # Additional attribute to compute deltaTime for animation purposes
        cmds.addAttr(self.nucleus, longName="lastFrameTime", attributeType="float", defaultValue=0.0)

        # Create expression to link textureOrigin with nucleus.windSpeed to move clouds
        # NOTE:
        # - opposite sign to translate them correctly with the axis
        # - scaling factor of 0.01
        expression = f"""
            float $deltaTime = time - {self.nucleus}.lastFrameTime;
            
            {self.cloud_container}.textureOriginX += - $deltaTime * ({self.nucleus}.windSpeed * {self.nucleus}.windDirectionX * 0.01);
            {self.cloud_container}.textureOriginY += - $deltaTime * ({self.nucleus}.windSpeed * {self.nucleus}.windDirectionY * 0.01);
            {self.cloud_container}.textureOriginZ += - $deltaTime * ({self.nucleus}.windSpeed * {self.nucleus}.windDirectionZ * 0.01);
            
            {self.nucleus}.lastFrameTime = time;
        """
        cmds.expression(name="WC:cloudMovementExpression", string=expression, alwaysEvaluate=True)

        # Create and assign rain material
        if not cmds.objExists('m_Rain'):
            rain_material = cmds.shadingNode('aiStandardSurface', asShader=True, name='m_Rain')
        else:
            rain_material = 'm_Rain'

        cmds.select(self.rain_particles)
        cmds.hyperShade(assign=rain_material)

        log(RAIN_PARTICLES_OBJECT_NAME + ' and ' + NUCLEUS_OBJECT_NAME + ' created successfully!')

        # Put the rain stuff inside the plugin group
        cmds.parent(self.rain_emitter, self.group)
        cmds.parent(self.rain_particles, self.group)
        cmds.parent(self.nucleus, self.group)

    def set_cloud_density(self, value):
        normalized_value = value / 100
        cmds.setAttr(f'{self.cloud_container}.opacityInputBias', normalized_value * 0.6)

    def add_cloud_density_keyframe(self):
        cmds.setKeyframe(f'{self.cloud_container}.opacityInputBias')

    def delete_cloud_density_keyframe(self):
        cmds.cutKey(f'{self.cloud_container}.opacityInputBias')

    def set_cloud_storminess(self, is_toggled):
        if is_toggled:
            cmds.setAttr(f'{self.cloud_container}.edgeDropoff', 0.499)
            cmds.setAttr(f'{self.cloud_container}.transparency', 0.01, 0.01, 0.01, type="double3")
        else:
            cmds.setAttr(f'{self.cloud_container}.edgeDropoff', 0.372)
            cmds.setAttr(f'{self.cloud_container}.transparency', 0.25, 0.25, 0.25, type="double3")

    def add_cloud_storminess_keyframe(self):
        cmds.setKeyframe(f'{self.cloud_container}.edgeDropoff')
        cmds.setKeyframe(f'{self.cloud_container}.transparency')

    def delete_cloud_storminess_keyframe(self):
        cmds.cutKey(f'{self.cloud_container}.edgeDropoff')
        cmds.setKeyframe(f'{self.cloud_container}.transparency')

    def set_cloud_details_amount(self, value):
        normalized_value = value / 100
        cmds.setAttr(f'{self.cloud_container}.frequencyRatio', normalized_value * 3.9 + 0.1)

    def add_cloud_details_keyframe(self):
        cmds.setKeyframe(f'{self.cloud_container}.frequencyRatio')

    def delete_cloud_details_keyframe(self):
        cmds.cutKey(f'{self.cloud_container}.frequencyRatio')

    def enable_rain(self, value):
        cmds.setAttr(f'{self.rain_emitter}.rate', value)

    def add_rain_enabled_keyframe(self):
        cmds.setKeyframe(f'{self.rain_emitter}.rate')

    def delete_rain_enabled_keyframe(self):
        cmds.cutKey(f'{self.rain_emitter}.rate')

    def set_wind_speed(self, value):
        cmds.setAttr(f'{self.nucleus}.windSpeed', value)

    def add_wind_speed_keyframe(self):
        cmds.setKeyframe(f'{self.nucleus}.windSpeed')

    def delete_wind_speed_keyframe(self):
        cmds.cutKey(f'{self.nucleus}.windSpeed')

    def set_wind_direction(self, value, axis):
        # Get previous values from the nucleus
        wind_direction = cmds.getAttr(f'{self.nucleus}.windDirection')[0]
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
        cmds.setAttr(f'{self.nucleus}.windDirectionX', wind_direction[0])
        cmds.setAttr(f'{self.nucleus}.windDirectionY', wind_direction[1])
        cmds.setAttr(f'{self.nucleus}.windDirectionZ', wind_direction[2])

    def add_wind_direction_keyframe(self):
        cmds.setKeyframe(f'{self.nucleus}.windDirection')

    def delete_wind_direction_keyframe(self):
        cmds.cutKey(f'{self.nucleus}.windDirection')