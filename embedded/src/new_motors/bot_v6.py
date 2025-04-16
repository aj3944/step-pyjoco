from motor2 import device, motor
import serial
import time


# import can 

# Initialize the device
uca = device("/dev/tty.usbserial-1110")
# uca = device("/dev/ttyUSB0")



class step_proto_6_bot():

	def __init__(self):
		self.left_hip_0 = motor(1, uca.port(), 1000 ) 
		self.left_hip_1 = motor(2, uca.port(), -500 ) 
		self.left_hip_2 = motor(3, uca.port(), 2500 ) 

		self.left_knee_0 = motor(4, uca.port(), 2000 ) 

		self.left_foot_0 = motor(5, uca.port(), 1000 ) 



		self.right_hip_0 = motor(11, uca.port(), 1000 ) 
		self.right_hip_1 = motor(12, uca.port(), -500 ) 
		self.right_hip_2 = motor(13, uca.port(), -2500 ) 

		self.right_knee_0 = motor(14, uca.port(), -1000 ) 

		self.right_foot_0 = motor(15, uca.port(), 0 ) 

	def home(self):

		self.left_hip_0.home()
		time.sleep(0.001)
		self.left_hip_1.home()
		time.sleep(0.001)
		self.left_hip_2.home()
		time.sleep(0.001)
		self.left_knee_0.home()
		time.sleep(0.001)
		self.left_foot_0.home()
		time.sleep(0.001)

		self.right_hip_0.home()
		time.sleep(0.001)
		self.right_hip_1.home()
		time.sleep(0.001)
		self.right_hip_2.home()
		time.sleep(0.001)
		self.right_knee_0.home()
		time.sleep(0.001)
		self.right_foot_0.home()
		time.sleep(0.001)

	def stop(self):

		self.left_hip_0.motor_stop()
		time.sleep(0.001)
		self.left_hip_1.motor_stop()
		time.sleep(0.001)
		self.left_hip_2.motor_stop()
		time.sleep(0.001)
		self.left_knee_0.motor_stop()
		time.sleep(0.001)
		self.left_foot_0.motor_stop()
		time.sleep(0.001)

		self.right_hip_0.motor_stop()
		time.sleep(0.001)
		self.right_hip_1.motor_stop()
		time.sleep(0.001) 
		self.right_hip_2.motor_stop()
		time.sleep(0.001)
		self.right_knee_0.motor_stop()
		time.sleep(0.001)
		self.right_foot_0.motor_stop()
		time.sleep(0.001)




# bot.stop()

# for i in range(1000):
# 	bot.stop()
	
# 	time.sleep(0.01)

if __name__ == "__main__": 
	bot = step_proto_6_bot()

	bot.stop()

	time.sleep(0.01) 

	bot.home()

	time.sleep(2)

	bot.stop()
