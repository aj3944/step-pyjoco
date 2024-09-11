from math import sin,cos,pi

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


class Controller():
	com_p = [0,0,0]
	com_v = [0,0,0]
	com_dv = [0,0,0]
	left_hip_yaw_ctrl = 0
	left_hip_pitch_ctrl = 0.5
	left_knee_pitch_ctrl = 0
	left_anke_roll_ctrl = 0.0

	unified_hip_yaw_ctrl = 0

	right_hip_yaw_ctrl = 0
	right_hip_pitch_ctrl = 0.5
	right_knee_pitch_ctrl = 0
	right_anke_roll_ctrl = 0


	def make_update(self,d):

		print(d.time)

		t_hat = d.time/3;

		# self.left_hip_pitch_ctrl = 0.5 + 0.2*sin(t_hat*0.5 + pi)**10;
		# self.right_hip_pitch_ctrl = 0.5 - 0.2*sin(t_hat*0.5)**10;

		self.left_hip_pitch_ctrl = 0.5 ;
		self.right_hip_pitch_ctrl = 0.5;


		self.left_hip_yaw_ctrl = 0.16*sin(t_hat);
		self.right_hip_yaw_ctrl = 0.16*sin(t_hat);

		# self.left_hip_pitch_ctrl = 0.4 + 0.05*sin(t_hat*2);
		# self.right_hip_pitch_ctrl = 0.4 + 0.05*cos(t_hat)*2;

		# self.right_anke_roll_ctrl = -0.2*sin(t_hat*0.5 + pi)**10;
		# self.left_anke_roll_ctrl = 0.2*sin(t_hat*0.5 + pi)**10;
		# self.right_anke_roll_ctrl = -0.2*sin(t_hat*0.5)**10;
		# self.right_anke_roll_ctrl = 0.05*cos(t_hat)*2;


		d.ctrl[lhy] = self.left_hip_yaw_ctrl; 
		d.ctrl[lhp] = -2*self.left_hip_pitch_ctrl;
		d.ctrl[lkp] = self.left_hip_pitch_ctrl + self.left_knee_pitch_ctrl;
		d.ctrl[lar] = self.left_anke_roll_ctrl;
		d.ctrl[rhy] = self.right_hip_yaw_ctrl; 
		d.ctrl[rhp] = -2*self.right_hip_pitch_ctrl;
		d.ctrl[rkp] = self.right_hip_pitch_ctrl + self.right_knee_pitch_ctrl;
		d.ctrl[rar] = self.right_anke_roll_ctrl;
