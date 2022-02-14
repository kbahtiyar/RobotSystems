import time
import sys
sys.path.append(r'/home/satyam/picar-x/lib/')
from utils import reset_mcu
reset_mcu()
from picarx_improved import Picarx

if __name__ == "__main__":
	px = Picarx()
	px.dir_servo_angle_calibration(5)
	px.camera_servo2_angle_calibration(0)
	px.camera_servo1_angle_calibration(-10)
	time.sleep(0.1)
	px.forward(50)
	time.sleep(3)
