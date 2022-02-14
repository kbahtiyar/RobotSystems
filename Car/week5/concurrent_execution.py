import sys
sys.path.append(r'/home/kaanb/RobotSystems/lib')
import rossros as ross
sys.path.append(r'/home/kaanb/RobotSystems/week4')
from week4 import Sensor, Interpreter, Controller
sys.path.append(r'/home/kaanb/RobotSystems/week5')
from ultrasonic import UltrasonicSensor, UltrasonicInterpreter, UltrasonicController
import concurrent.futures

if __name__ == "__main__":
    sensor = Sensor()
    interpreter = Interpreter(sensitivity = 1.5, polarity= -1)
    controller = Controller(scalingFactor=15)
    
    sensor_ultrasonic = UltrasonicSensor()
    interpreter_ultrasonic = UltrasonicInterpreter(limit=10) 
    controller_ultrasonic = UltrasonicController(speed=30)  
    
    sensor_bus = ross.Bus([1, 1, 1], "Grayscale Sensor Bus")
    interpreter_bus = ross.Bus(0, "Grayscale Interpreter Bus")
    sensor_ultrasonic_bus = ross.Bus(-1, "Ultrasonic Sensor Bus")
    interpreter_ultrasonic_bus = ross.Bus(1, "Ultrasonic Interpreter Bus")
    term_bus = ross.Bus(0, "Termination Bus")
    
    sensor_p = ross.Producer(sensor.val_buffer, sensor_bus, 0.05, term_bus, "Grayscale producer")
    sensor_ultrasonic_p = ross.Producer(sensor_ultrasonic.val_buffer, sensor_ultrasonic_bus, 0.05, term_bus, "Ultrasonic producer")
    
    interpreter_cp = ross.ConsumerProducer(interpreter.edge_detection, sensor_bus, interpreter_bus, 0.05, term_bus,
                                "Grayscale Interpreter")
    interpreter_ultrasonic_cp = ross.ConsumerProducer(interpreter_ultrasonic.detection, sensor_ultrasonic_bus, interpreter_ultrasonic_bus, 0.05, term_bus,
                                "Ultrasonic Interpreter")
    
    controller_c = ross.Consumer(controller.steering, interpreter_bus, 0.05, term_bus, "Grayscale Controller")
    controller_ultrasonic_c = ross.Consumer(controller_ultrasonic.control, interpreter_ultrasonic_bus, 0.05, term_bus, "Ultrasonic Controller")
    term_timer = ross.Timer(term_bus, 5, 0.05, term_bus, "Termination Timer")
     
     
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
        eGrySensor = executor.submit(sensor_p)
        eGryInterp = executor.submit(interpreter_cp)
        eGryCont = executor.submit(controller_c)
        eUltSensor = executor.submit(sensor_ultrasonic_p)
        eUltInterp = executor.submit(interpreter_ultrasonic_cp)
        eUltCont = executor.submit(controller_ultrasonic_c)
        eTimer = executor.submit(term_timer)

    eGrySensor.result()
    eGryInterp.result()
    eGryCont.result()
    eUltSensor.result()
    eUltInterp.result()
    eUltCont.result()
    eTimer.result()