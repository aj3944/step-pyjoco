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


print(dir(mujoco.mjtVisFlag))

lipm_lqr = Controller()

with mujoco.viewer.launch_passive(m, d) as viewer:
	# Close the viewer automatically after 30 wall-seconds.
	start = time.time()
	# mujoco.set_mjcb_time = True
	delta_y = 0;


	delt = 0
	step_prev = step_start = 0;
	with viewer.lock():
		viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = 1
		viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTFORCE] = 1
		viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_AUTOCONNECT] = 1
		viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_COM] = 1


	while viewer.is_running() and time.time() - start < 300:
		elasped = time.time() - start

		# mj_step can be replaced with code that also evaluates
		# a policy and applies a control signal before stepping the physics.

		mujoco.mj_step(m, d)
		lipm_lqr.make_update(0,d)
		# print(elasped)
		# Pick up changes to the physics state, apply perturbations, update options from GUI.
		viewer.sync()
		# time.sleep(0.01)
		# Rudimentary time keeping, will drift relative to wall clock.
		time_until_next_step = m.opt.timestep - (time.time() - step_start)
		if time_until_next_step > 0:
			time.sleep(time_until_next_step)
