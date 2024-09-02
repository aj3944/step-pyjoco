import time

import mujoco
import mujoco.viewer
from math import sin,pi

import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.widgets import Button, Slider

scene_option = mujoco.MjvOption()



scene_option.flags[mujoco.mjtVisFlag.mjVIS_CONTACTFORCE] = True


gyro_y_reads = [0]*100


fig, ax = plt.subplots()
line, = ax.plot(np.random.randn(100)*1)
plt.show(block=False)

fig.subplots_adjust(left=0.25, bottom=0.75)
axfreqL = fig.add_axes([0.25, 0.1, 0.65, 0.03])
axfreqS = fig.add_axes([0.25, 0.2, 0.65, 0.03])
axfreqA = fig.add_axes([0.25, 0.0, 0.65, 0.03])
axfreqM = fig.add_axes([0.25, 0.3, 0.65, 0.03])
freq_sliderS = Slider(
    ax=axfreqS,
    label='S',
    valmin=-1,
    valmax=1,
    valinit=0,
)
freq_sliderL = Slider(
    ax=axfreqL,
    label='L',
    valmin=-1,
    valmax=1,
    valinit=0,
)
freq_sliderA = Slider(
    ax=axfreqA,
    label='A',
    valmin=-1,
    valmax=1,
    valinit=0,
)
freq_sliderM = Slider(
    ax=axfreqM,
    label='M',
    valmin=-1,
    valmax=1,
    valinit=0,
)


m = mujoco.MjModel.from_xml_path('scene.xml')
d = mujoco.MjData(m)


beta_P = 0
beta_I = 0
beta_D = 0
global left_hip_yaw_ctrl,left_hip_pitch_ctrl,left_knee_pitch_ctrl,left_anke_roll_ctrl
global right_hip_yaw_ctrl,right_hip_pitch_ctrl,right_knee_pitch_ctrl,right_anke_roll_ctrl

left_hip_yaw_ctrl = 0
left_hip_pitch_ctrl = 0.5
left_knee_pitch_ctrl = 0
left_anke_roll_ctrl = 0

unified_hip_yaw_ctrl = 0

right_hip_yaw_ctrl = 0
right_hip_pitch_ctrl = 0.5
right_knee_pitch_ctrl = 0
right_anke_roll_ctrl = 0


left_hip_yaw = 0
left_hip_pitch = 1
left_knee_pitch = 2
left_ankle_roll = 3
right_hip_yaw = 4
right_hip_pitch = 5
right_knee_pitch = 6
right_ankle_roll = 7


lhy = 0
lhp =1
lkp = 2
lar = 3
rhy = 4
rhp = 5
rkp = 6
rar = 7

def updateS(val):
    global left_hip_pitch_ctrl
    print("val")
    left_hip_pitch_ctrl = val
def updateL(val):
    global left_knee_pitch_ctrl
    print("val")
    left_knee_pitch_ctrl = val
def updateA(val):
    global left_anke_roll_ctrl
    print("val")
    left_anke_roll_ctrl = val
def updateM(val):
    global left_hip_yaw_ctrl
    print("val")
    left_hip_yaw_ctrl = val

freq_sliderS.on_changed(updateS)
freq_sliderL.on_changed(updateL)
freq_sliderA.on_changed(updateA)
freq_sliderM.on_changed(updateM)

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
    omega =6
    
    # pid_y = delta_y - int_y*0.01;

    # ctrl_value = gain_p*beta_P + gain_d*beta_D + gain_i*beta_I
    # ctrl_value = 0
    unified_hip_yaw_ctrl = sin(omega*step_start)*0.11

    left_hip_pitch_ctrl = 0.6 + sin(omega*step_start)*0.002
    right_hip_pitch_ctrl = 0.6 + sin(pi + omega*step_start)*0.002
    left_knee_pitch_ctrl = 0.005 + sin(pi + omega*step_start)*0.002
    right_knee_pitch_ctrl = 0.005 + sin(omega*step_start)*0.002



    # right_hip_pitch_ctrl = 0.5
    # left_anke_roll_ctrl =  0
    # right_anke_roll_ctrl =  0

    d.ctrl[lhy] = unified_hip_yaw_ctrl 
    d.ctrl[lhp] = -2*left_hip_pitch_ctrl - left_knee_pitch_ctrl
    d.ctrl[lkp] = left_hip_pitch_ctrl + left_knee_pitch_ctrl
    d.ctrl[lar] = left_anke_roll_ctrl
    d.ctrl[rhy] = unified_hip_yaw_ctrl 
    d.ctrl[rhp] = -2*right_hip_pitch_ctrl
    d.ctrl[rkp] = right_hip_pitch_ctrl  + right_knee_pitch_ctrl
    d.ctrl[rar] = right_anke_roll_ctrl
    # print(left_hip_yaw_ctrl)
    # print(left_knee_pitch_ctrl)
    # print(left_anke_roll_ctrl)

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