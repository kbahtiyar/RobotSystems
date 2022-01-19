import sys
sys.path.append(r'/home/pi/picar-x/lib')
from utils import reset_mcu
reset_mcu()

import logging
from logdecorator import log_on_start , log_on_end , log_on_error
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
from picarx_improved import Picarx
import time

@log_on_start(logging.DEBUG, "Forward&Backward motion is started.")
@log_on_end(logging.DEBUG, "Successful")
def forward_backward(px):
	px.forward(30)
	time.sleep(1)
	px.forward(0)
	time.sleep(0.01)
	px.backward(30)
	time.sleep(1)
	px.backward(0)
	time.sleep(1)

@log_on_start(logging.DEBUG, "Parallel parking (left) motion is started.")
@log_on_end(logging.DEBUG, "Successful")
def parallel_left(px):
	px.forward(30)
	time.sleep(0.5)
	px.forward(0)
	time.sleep(0.01)
	px.set_dir_servo_angle(-20)
	time.sleep(0.2)
	px.backward(30)
	time.sleep(0.75)
	px.backward(0)
	time.sleep(0.01)
	px.set_dir_servo_angle(20)
	time.sleep(0.2)
	px.backward(30)
	time.sleep(0.5)
	px.backward(0)
	time.sleep(0.01)
	px.set_dir_servo_angle(30)
	time.sleep(0.2)
	px.backward(30)
	time.sleep(0.5)
	px.backward(0)
	time.sleep(0.01)
	px.set_dir_servo_angle(-10)
	px.forward(30)
	time.sleep(0.5)
	px.forward(0)
	time.sleep(0.01)
	px.set_dir_servo_angle(30)
	time.sleep(0.2)
	px.forward(30)
	time.sleep(0.5)
	px.forward(0)
	time.sleep(0.01)
	px.set_dir_servo_angle(0)
	time.sleep(0.2)
	px.forward(10)
	time.sleep(0.25)
	px.forward(0)
	time.sleep(0.01)

@log_on_start(logging.DEBUG, "Parallel parking (right) motion is started.")
@log_on_end(logging.DEBUG, "Successful")
def parallel_right(px):
	px.forward(30)
	time.sleep(0.5)
	px.forward(0)
	time.sleep(0.01)
	px.set_dir_servo_angle(20)
	time.sleep(0.2)
	px.backward(30)
	time.sleep(0.75)
	px.backward(0)
	time.sleep(0.01)
	px.set_dir_servo_angle(-20)
	time.sleep(0.2)
	px.backward(30)
	time.sleep(0.5)
	px.backward(0)
	time.sleep(0.01)
	px.set_dir_servo_angle(-30)
	time.sleep(0.2)
	px.backward(30)
	time.sleep(0.5)
	px.backward(0)
	time.sleep(0.01)
	px.set_dir_servo_angle(10)
	px.forward(30)
	time.sleep(0.5)
	px.forward(0)
	time.sleep(0.01)
	px.set_dir_servo_angle(-30)
	time.sleep(0.2)
	px.forward(30)
	time.sleep(0.5)
	px.forward(0)
	time.sleep(0.01)
	px.set_dir_servo_angle(0)
	time.sleep(0.2)
	px.forward(10)
	time.sleep(0.25)
	px.forward(0)
	time.sleep(0.01)

@log_on_start(logging.DEBUG, "K-turning motion is started.")
@log_on_end(logging.DEBUG, "Successful")
def k_turning(px):
	px.forward(30)
	time.sleep(0.5)
	px.forward(0)
	time.sleep(0.01)
	px.set_dir_servo_angle(-45)
	time.sleep(0.1)
	px.forward(30)
	time.sleep(0.75)
	px.forward(0)
	time.sleep(0.01)
	px.set_dir_servo_angle(45)
	time.sleep(0.1)
	px.backward(30)
	time.sleep(0.5)
	px.backward(0)
	time.sleep(0.01)
	px.set_dir_servo_angle(-45)
	time.sleep(0.1)
	px.forward(30)
	time.sleep(0.80)
	px.forward(0)
	time.sleep(0.01)
	px.set_dir_servo_angle(0)
	time.sleep(0.1)
	px.forward(30)
	time.sleep(0.25)
	px.forward(0)
	time.sleep(0.01)

	

if __name__ == "__main__":
	px = Picarx()
	print("Enter 1 for Forward and Backward")
	print("Enter 2 for Parallel Parking (Right)")
	print("Enter 3 for Parallel Parking (Left)")
	print("Enter 4 for K-Turning")
	print("Enter 0 for Exit")
	inp = input()
	print(inp)
	while(inp != '0'):

		px.set_dir_servo_angle(0)
		if inp=='1':
			forward_backward(px)
		elif inp=='2':
			parallel_right(px)
		elif inp=='3':
			parallel_left(px)
		elif inp=='4':
			k_turning(px)
		elif inp=='0':
			break
		else:
			print("Enter valid selection")
		print("Enter 1 for Parallel Parking Right")
		print("Enter 2 for Parallel Parking Left")
		print("Enter 3 for Three Point Turning")
		print("Enter 4 for Forward and Backward")
		print("Enter 5 for Exit")
		inp = input()
		print(inp)
		time.sleep(1)

















