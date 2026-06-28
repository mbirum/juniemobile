from enum import Enum, auto
import motor_sequencer
import time
import threading

class MotorAxis(Enum):
    X = auto()
    Y = auto()

class MotorStepType(Enum):
    MOVE = auto()
    WAIT = auto()

class MotorWait(Enum):
    SHORT = 0.1
    MEDIUM = 0.35
    LONG = 0.75


class MotorStep:
    step_type: MotorStepType
    action = None


class Motor:

    y_axis_pins = [11,13,15,37]
    x_axis_pins = [16,18,22,32]
    axis: MotorAxis = None
    step_queue: MotorStep[] = []
    control_pins = [0, 0, 0, 0]
    default_distance = 40
    default_move_rate = 0.001
    motor_running = False


    def __init__(self, axis: MotorAxis):
        self.axis = axis
        if axis == MotorAxis.X:
            self.control_pins = x_axis_pins
        else if axis == MotorAxis.Y:
            self.control_pins = y_axis_pins
        set_up_pins()


    def set_up_pins(self):
        GPIO.setmode(GPIO.BOARD)
        for pin in self.control_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)


    def queue(self, step):
        print(f'queuing {step.step_type} step')
        step_queue.push(step)


    def dequeue(self):
        step_to_remove = step_queue[0]
        if step_to_remove:
            print(f'removing {step_to_remove.step_type} step')
            step_queue.pop(0)
        else:
            print(f'step_queue is already empty')


    def wait(self, seconds: float):
        time.sleep(seconds)
    

    def move(self, sequence, distance = default_distance, rate = default_move_rate):
        for i in range(int(distance)):
            for step in range(len(sequence)):
                x_step = sequence[step % len(sequence)]
                for pin_idx in range(4):
                    GPIO.output(leftright_pins[pin_idx], x_step[pin_idx])
                time.sleep(rate)


    def execute(self):
        if not self.motor_running:
            self.motor_running = True
            # threading.Thread(target=_kb_loop, daemon=True)
            while step_queue:
                step = step_queue[0]
                if step:
                    if step.step_type == MotorStepType.WAIT:
                        wait(step.action)
                    else if step.step_type == MotorStepType.MOVE:
                        move(step.action)
                    else:
                        print(f'invalid step: {step.action}')
                    self.dequeue()
            self.motor_running = False


    # def up(self, wait: MotorWait):
    #     if axis == MotorAxis.Y:


    # def down(self):


    # def left(self):


    # def right(self):
