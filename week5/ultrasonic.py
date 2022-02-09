import sys
sys.path.append(r'/home/kaanb/RobotSystems/lib')
import atexit
from picarx_improved import Picarx
import numpy
import time

class UltrasonicSensor(Picarx):
    def __init__(self):
        super().__init__()

    def get_readings(self):
        return self.Get_distance()

    def val_buffer(self):
        readings = []
        for i in range(10):
            readings.append(self.get_readings())
        average_readings = numpy.mean(readings, axis=0)
        return average_readings
        #mean of 10 readings
        

class UltrasonicInterpreter(object):
    def __init__(self, limit=10):
        # Stopping limit in cm
        self.limit = limit

    # Stop the car based on the stopping limit
    def detection(self, distance):
        if distance < 0:
            return True
        elif distance > self.limit:
            return True
        else:
            return False


class UltrasonicController(Picarx):
    def __init__(self,speed=30):
        super().__init__()
        self.speed = speed
    def control(self, detected):
        if detected == True:
            self.forward(self.speed)
            time.sleep(0.05)
        else:
            self.forward(0)
            time.sleep(0.05)

if __name__ == "__main__":
    time.sleep(1)
    sensor = UltrasonicSensor()
    interpreter = UltrasonicInterpreter() 
    controller = UltrasonicController()

    try:
        while True:
            controller.control(interpreter.detection(sensor.val_buffer()))
    except:
        print("Error in execution")
        atexit.register(controller.stop)

    finally:
        atexit.register(controller.stop)