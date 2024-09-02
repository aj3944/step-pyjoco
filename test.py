import time

import mujoco
import mujoco.viewer
from math import sin

import matplotlib.pyplot as plt
import numpy as np
import time


gyro_y_reads = [0]*100


fig, ax = plt.subplots()
line, = ax.plot(np.random.randn(100)*1)
plt.show(block=False)


m = mujoco.MjModel.from_xml_path('scene.xml')
d = mujoco.MjData(m)


beta_P = 0
beta_I = 0
beta_D = 0



left_hip_yaw = 0
left_hip_pitch = 1
left_knee_pitch = 2
left_ankle_roll = 3
right_hip_yaw = 4
right_hip_pitch = 5
right_knee_pitch = 6
right_ankle_roll = 7

lhy = 0
lhp = 1
lkp = 2
lar = 3
rhy = 4
rhp = 5
rkp = 6
rar = 7



with mujoco.viewer.launch_passive(m, d) as viewer:
  # Close the viewer automatically after 30 wall-seconds.
  start = time.time()
  
  delta_y = 0;

  while viewer.is_running() and time.time() - start < 300:
    step_start = time.time()

    # mj_step can be replaced with code that also evaluates
    # a policy and applies a control signal before stepping the physics.
    mujoco.mj_step(m, d)

    # for i in range(len(d.ctrl)):
    # 	d.ctrl[i] = 0




    g_x,g_y,g_z = d.sensordata[0],d.sensordata[1],d.sensordata[2]
    a_x,a_y,a_z = d.sensordata[0],d.sensordata[1],d.sensordata[2]


    gyro_y_reads.pop(0)
    gyro_y_reads.append(g_y)


    delta_y += g_y;

    beta_P += g_y;
    beta_I = sum(gyro_y_reads)/len(gyro_y_reads);
    beta_D = g_y

    gain_p = 0.8
    gain_i = 0.3
    gain_d = 0.3

    # print(int_y)

    
    # pid_y = delta_y - int_y*0.01;

    ctrl_value = gain_p*beta_P + gain_d*beta_D + gain_i*beta_I
    # ctrl_value = 0


    # d.ctrl[lhy] = 0
    d.ctrl[lhp] = ctrl_value
    d.ctrl[lkp] = ctrl_value
    # d.ctrl[lar] = 0
    # d.ctrl[rhy] = 0
    d.ctrl[rhp] = ctrl_value
    d.ctrl[rkp] = ctrl_value
    # d.ctrl[rar] = 0
    
    # print(
    # 	(d.sensordata)
    # 	)
    line.set_ydata(gyro_y_reads)
    ax.draw_artist(ax.patch)
    ax.draw_artist(line)
    fig.canvas.update()
    fig.canvas.flush_events()

    # Example modification of a viewer option: toggle contact points every two seconds.
    with viewer.lock():
      viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = int(d.time % 2)

    # Pick up changes to the physics state, apply perturbations, update options from GUI.
    viewer.sync()

    # Rudimentary time keeping, will drift relative to wall clock.
    time_until_next_step = m.opt.timestep - (time.time() - step_start)
    if time_until_next_step > 0:
      time.sleep(time_until_next_step)