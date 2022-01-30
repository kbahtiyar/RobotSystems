from Bus import Bus
import sys
sys.path.append(r'/home/kaanb/RobotSystems/lib')
from week4 import Sensor, Interpreter, Controller
import time
import concurrent.futures
import atexit

if __name__ == "__main__":
    sensor = Sensor()
    interpreter = Interpreter(sensitivity = 1.5, polarity= -1)
    controller = Controller(scalingFactor=15)
    sensor_bus = Bus()
    interpreter_bus = Bus()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        eSensor = executor.submit(sensor.producer, sensor_bus, 0.05)
        eInterpreter = executor.submit(interpreter.consumer_producer, sensor_bus, interpreter_bus, 0.05)
        eController = executor.submit(controller.consumer, interpreter_bus, 0.05)

    eSensor.result()
    eInterpreter.result()
    eController.result()