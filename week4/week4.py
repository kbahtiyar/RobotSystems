import sys
sys.path.append(r'/home/kaanb/RobotSystems/lib')
import time
import numpy
from picarx_improved import Picarx
import atexit


try:
    from ezblock import *
    from ezblock import __reset_mcu__
    __reset_mcu__()
    time.sleep(0.01)
except ImportError:
    print("This computer does not appear to be a PiCar-X system (/opt/ezblock is not present). Shadowing hardware calls with substitute functions")
    from sim_ezblock import *

class Sensor(Picarx):
    def __init__(self):
        super().__init__()
        self.C0 = ADC("A0")
        self.C1 = ADC("A1")
        self.C2 = ADC("A2")
        # ADC values for grayscale module

    def get_adc_value(self):
        adc_value_list = []
        adc_value_list.append(self.C0.read())
        adc_value_list.append(self.C1.read())
        adc_value_list.append(self.C2.read())
        return adc_value_list

    def val_buffer(self):
        adc_readings = []
        norm_adc_readings = []
        for i in range(10):
            adc_readings.append(self.get_adc_value())
        average_readings = numpy.mean(adc_readings, axis=0)
        sum_readings = numpy.sum(average_readings)
        for i in range(3):
            norm_adc_readings.append(average_readings[i] / sum_readings)
        return norm_adc_readings
        #normalized mean of 10 readings

    def producer(self, sensor_bus, delay):
        while True:
            data = self.val_buffer()
            sensor_bus.write(data)
            time.sleep(delay)

class Interpreter():
    def __init__(self, sensitivity = 1.5, polarity= -1):
        super().__init__()
        self.sensitivity = sensitivity
        self.polarity = polarity
        # Sensitivity: Ratio of light to dark readings of sensor (Dark surface: lower readings, Light surface: higher readings)
        # Polarity: -1 for light line, 1 for dark line


    def edge_detection(self,data):
        adc_value_norm = data
        hard_right = 0
        hard_left = 0
        if self.polarity == -1:
            read1 = adc_value_norm[1]/adc_value_norm[0]
            read2 = adc_value_norm[1]/adc_value_norm[2]
            if (adc_value_norm[0] > self.sensitivity * adc_value_norm[1]) and (adc_value_norm[0] > self.sensitivity * adc_value_norm[2]):
                hard_right = 1
            if (adc_value_norm[2] > self.sensitivity * adc_value_norm[1]) and (adc_value_norm[2] > self.sensitivity * adc_value_norm[0]):
                hard_left = 1
        else:
            read1 = adc_value_norm[0]/adc_value_norm[1]
            read2 = adc_value_norm[2]/adc_value_norm[1]
            if adc_value_norm[1] > self.sensitivity * adc_value_norm[0] and adc_value_norm[2] > self.sensitivity * adc_value_norm[0]:
                hard_right = 1
            if adc_value_norm[1] > self.sensitivity * adc_value_norm[2] and adc_value_norm[0] > self.sensitivity * adc_value_norm[2]:
                hard_left = 1

        if read1>self.sensitivity and read2>self.sensitivity:
            deg = 0
            dir = [False, True, False]
        elif read1>self.sensitivity and read2<self.sensitivity:
            deg = read1-read2
            dir = [True, False, False]
        elif read1<self.sensitivity and read2>self.sensitivity:
            deg = read2-read1
            dir = [False, False, True]
        elif hard_right == 1:
            deg = 2 * adc_value_norm[0] / (adc_value_norm[1] + adc_value_norm[2])
            dir = [False, False, True]
        elif hard_left == 1:
            deg = 2 * adc_value_norm[2] / (adc_value_norm[1] + adc_value_norm[0])
            dir = [True, False, False]
        else:
            deg = 0
            dir = [False, False, False]
        return dir, deg

    def consumer_producer(self, sensor_bus, interpreter_bus, delay):
        while True:
            data = sensor_bus.read()
            data = self.edge_detection(data)
            interpreter_bus.write(data)
            time.sleep(delay)

class Controller(Picarx):
    def __init__(self, scalingFactor=15):
        super().__init__()
        self.scalingFactor = scalingFactor

    def steering(self,direction,degree):
        steer = int(self.scalingFactor * degree)

        if direction == [False, False, True]:
            steer = -1 * steer
        if direction == [False, False, False]:
            self.stop()
            self.set_dir_servo_angle(0)
            time.sleep(0.01)
        else:
            self.set_dir_servo_angle(steer)
            time.sleep(0.01)
        self.forward(30)
        time.sleep(0.05)

    def consumer(self, interpreter_bus, delay):
        while True:
            data = interpreter_bus.read()
            direction, degree = data[0], data[1]
            self.control(direction, degree)
            time.sleep(delay)

if __name__ == "__main__":

    time.sleep(3)
    sensor = Sensor()
    processor = Interpreter(sensitivity = 1.5, polarity= -1)
    controller = Controller(scalingFactor=15)
    data = None
    direction = None
    degree = None
    try:
        while True:
            data = sensor.val_buffer()
            data = processor.edge_detection(data)
            direction, degree = data[0], data[1]
            controller.steering(direction, degree)
    finally:
        atexit.register(controller.stop)