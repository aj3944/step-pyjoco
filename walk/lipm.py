from math import sin,cos,pi,floor

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


	curr_pos = []
	goal_pos = []

	controls = [0]*8
	step = 0;

	def make_update(self,t = None,d = None):

		if d is None and t is None:
			raise

		if d:
			print(d.time)

			if d.time < 0:
				return 0
			t = d.time
		t_hat = t/3;

		self.step += 0.003

		step_h = floor(self.step/pi);

		flex_l, flex_r = 0, 0
		if step_h % 2 == 0:
			march_l = -sin(self.step)*0.15
			march_r = 0
			# flex_l = flex_l*0.99
			# flex_r = -cos(self.step)*0.1
		else:
			march_l = 0
			march_r = sin(self.step)*0.15
			# flex_l = cos(self.step)*0.1
			# flex_r = flex_r*0.99
		# march_l_val = march_l
		# self.left_hip_pitch_ctrl = march_l;
		# self.right_hip_pitch_ctrl = march_r;
		flex_l = cos(self.step+0.75*pi)*0.02
		flex_r = -cos(self.step+0.75*pi)*0.02
		# self.left_hip_pitch_ctrl = 0.5 ;
		# self.right_hip_pitch_ctrl = 0.5;


		self.left_hip_yaw_ctrl = 0.18*sin(self.step);
		self.right_hip_yaw_ctrl = 0.18*sin(self.step);



		# self.left_hip_pitch_ctrl = 0.4 + 0.05*sin(t_hat*2);
		# self.right_hip_pitch_ctrl = 0.4 + 0.05*cos(t_hat)*2;

		# self.right_anke_roll_ctrl = -0.2*sin(t_hat*0.5 + pi)**10;
		# self.left_anke_roll_ctrl = 0.2*sin(t_hat*0.5 + pi)**10;
		# self.right_anke_roll_ctrl = -0.2*sin(t_hat*0.5)**10;
		# self.right_anke_roll_ctrl = 0.05*cos(t_hat)*2;

		# self.controls[lhy] = self.left_hip_yaw_ctrl; 
		# self.controls[lhp] = -2*self.left_hip_pitch_ctrl + march_l;
		# self.controls[lkp] = self.left_hip_pitch_ctrl + self.left_knee_pitch_ctrl - 2*march_l;
		# self.controls[lar] = self.left_anke_roll_ctrl + flex_l;
		# self.controls[rhy] = self.right_hip_yaw_ctrl; 
		# self.controls[rhp] = -2*self.right_hip_pitch_ctrl + march_r;
		# self.controls[rkp] = self.right_hip_pitch_ctrl + self.right_knee_pitch_ctrl - 2*march_r;
		# self.controls[rar] = self.right_anke_roll_ctrl + flex_r;

		# self.controls[lhy] = 0;
		self.controls[lhp] = self.left_hip_yaw_ctrl;
		# self.controls[lkp] = 0.2;
		# # self.controls[lar] = 0.2;
		# self.controls[rhy] = 0;
		self.controls[rhp] = self.left_hip_yaw_ctrl;
		# self.controls[rkp] = 0.2;
		# self.controls[rar] = 0.2;

		if d:
			d.ctrl[lhy] = self.controls[lhy]
			d.ctrl[lhp] = self.controls[lhp]
			d.ctrl[lkp] = self.controls[lkp]
			d.ctrl[lar] = self.controls[lar]
			d.ctrl[rhy] = self.controls[rhy]
			d.ctrl[rhp] = self.controls[rhp]
			d.ctrl[rkp] = self.controls[rkp]
			d.ctrl[rar] = self.controls[rar]

		return self.controls