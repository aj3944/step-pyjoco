from dm_control import mjcf
from dm_control import suite
from dm_control import viewer


# class Arm:

#   def __init__(self, name):
#     self.mjcf_model = mjcf.RootElement(model=name)

#     self.upper_arm = self.mjcf_model.worldbody.add('body', name='upper_arm')
#     self.shoulder = self.upper_arm.add('joint', name='shoulder', type='ball')
#     self.upper_arm.add('geom', name='upper_arm', type='capsule',
#                        pos=[0, 0, -0.15], size=[0.045, 0.15])

#     self.forearm = self.upper_arm.add('body', name='forearm', pos=[0, 0, -0.3])
#     self.elbow = self.forearm.add('joint', name='elbow',
#                                   type='hinge', axis=[0, 1, 0])
#     self.forearm.add('geom', name='forearm', type='capsule',
#                      pos=[0, 0, -0.15], size=[0.045, 0.15])

# class UpperBody:

#   def __init__(self):
#     self.mjcf_model = mjcf.RootElement()
#     self.mjcf_model.worldbody.add(
#         'geom', name='torso', type='box', size=[0.15, 0.045, 0.25])
#     left_shoulder_site = self.mjcf_model.worldbody.add(
#         'site', size=[1e-6]*3, pos=[-0.15, 0, 0.25])
#     right_shoulder_site = self.mjcf_model.worldbody.add(
#         'site', size=[1e-6]*3, pos=[0.15, 0, 0.25])

#     self.left_arm = Arm(name='left_arm')
#     left_shoulder_site.attach(self.left_arm.mjcf_model)

#     self.right_arm = Arm(name='right_arm')
#     right_shoulder_site.attach(self.right_arm.mjcf_model)


# The basic mujoco wrapper.
from dm_control import mujoco

# Access to enums and MuJoCo library functions.
from dm_control.mujoco.wrapper.mjbindings import enums
from dm_control.mujoco.wrapper.mjbindings import mjlib

# PyMJCF
from dm_control import mjcf

# Composer high level imports
from dm_control import composer
from dm_control.composer.observation import observable
from dm_control.composer import variation

# Imports for Composer tutorial example
from dm_control.composer.variation import distributions
from dm_control.composer.variation import noises
from dm_control.locomotion.arenas import floors

# Control Suite
from dm_control import suite

# Run through corridor example
from dm_control.locomotion.walkers import cmu_humanoid
from dm_control.locomotion.arenas import corridors as corridor_arenas
from dm_control.locomotion.tasks import corridors as corridor_tasks


# General
import copy
import os
import itertools
from IPython.display import clear_output
import numpy as np


# Graphics-related
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from IPython.display import HTML
import PIL.Image

walker = cmu_humanoid.CMUHumanoidPositionControlledV2020(
    observable_options={'egocentric_camera': dict(enabled=True)})

arena = corridor_arenas.WallsCorridor(
    wall_gap=3.,
    wall_width=distributions.Uniform(2., 3.),
    wall_height=distributions.Uniform(2.5, 3.5),
    corridor_width=4.,
    corridor_length=30.,
)

task = corridor_tasks.RunThroughCorridor(
    walker=walker,
    arena=arena,
    walker_spawn_position=(0.5, 0, 0),
    target_velocity=3.0,
    physics_timestep=0.005,
    control_timestep=0.03,
)

env = composer.Environment(
    task=task,
    time_limit=10,
    random_state=np.random.RandomState(42),
    strip_singleton_obs_buffer_dim=True,
)
env.reset()
pixels = []
for camera_id in range(3):
  pixels.append(env.physics.render(camera_id=camera_id, width=240))
img = PIL.Image.fromarray(np.hstack(pixels))

img.show()


