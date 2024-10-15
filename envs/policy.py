import os
import sys
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name + "/walk")
from lipm import Controller
from dm_control import mjcf
from dm_control import suite
from dm_control import viewer

import numpy as np

from step import SUITE

env = SUITE["walk"](100)
action_spec = env.action_spec()


lipm_lqr = Controller()

physics = env.physics
k = 0 
def lipm_policy(time_step):
	global k
	k += 0.001
	t = physics.time()
	r = time_step.reward
	# print(r)
	# print(k)
	q = lipm_lqr.make_update(k)
	return q 


viewer.launch(env,  policy=lipm_policy)
