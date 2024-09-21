import time

import mujoco
import mujoco.viewer
from math import sin,pi

import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.widgets import Button, Slider

from lipm import Controller

m = mujoco.MjModel.from_xml_path('../scene.xml')
d = mujoco.MjData(m)

lipm_lqr = Controller()

with mujoco.viewer.launch_passive(m, d) as viewer:
	# Close the viewer automatically after 30 wall-seconds.
	start = time.time()
	delta_y = 0;

	delt = 0
	step_prev = step_start = 0;
	with viewer.lock():
		viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = 1
		viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTFORCE] = 1
		viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_AUTOCONNECT] = 1

	while viewer.is_running() and time.time() - start < 300:
		# mj_step can be replaced with code that also evaluates
		# a policy and applies a control signal before stepping the physics.
		mujoco.mj_step(m, d)
		lipm_lqr.make_update(d)
		# Pick up changes to the physics state, apply perturbations, update options from GUI.
		viewer.sync()
