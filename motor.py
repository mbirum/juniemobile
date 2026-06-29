import motor_sequencer
import time
import threading
import RPi.GPIO as GPIO

default_distance = 10
default_move_rate = 0.001

class MotorPosition:
    position = 0
    _lock = threading.Lock()

    def write(self, position):
        if position >= -1 and position <= 1:
            with self._lock:
                self.position = position
        else:
            print(f'error writing position: {position}')

    def get(self):
        return self.position


class Motor:

    position = MotorPosition()
    is_free = True
    degree = 0

    # x_axis_pins = [16,18,22,32]
    # y_axis_pins = [11,13,15,37]
    x_axis_pins = [11,13,15,37]
    y_axis_pins = [16,18,22,32]
    control_pins = [0, 0, 0, 0]


    def __init__(self, axis):
        self.axis = axis
        if axis == "x":
            self.control_pins = self.x_axis_pins
        elif axis == "y":
            self.control_pins = self.y_axis_pins
        self.set_up_pins()


    def set_up_pins(self):
        GPIO.setmode(GPIO.BOARD)
        for pin in self.control_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)


    def get_sleep_duration(self, duration_digit):
        if duration_digit == 1:
            return 0.1
        elif duration_digit == 2:
            return 0.35
        elif duration_digit == 3:
            return 0.75
    

    def free(self):
        return self.is_free

    def motor_sequence(self, direction, distance = default_distance, budge = False, rate = default_move_rate):
        print(f'{self.axis} motor_sequence:: direction={direction} distance={distance} rate={rate}')
        sequence = motor_sequencer.forward()
        if direction < 0:
            sequence = motor_sequencer.backward()
        self.is_free = False
        for i in range(int(distance)):
            for step in range(len(sequence)):
                x_step = sequence[step % len(sequence)]
                for pin_idx in range(4):
                    GPIO.output(self.control_pins[pin_idx], x_step[pin_idx])
                time.sleep(rate)
            if not budge:
                self.degree = self.degree + direction
        self.is_free = True


    def move(self, direction, duration):
        new_position = self.position.get() + direction
        if new_position < -1 or new_position > 1:
            print(f'cannot move past position {self.position.get()}')
            return

        self.position.write(new_position)
        self.motor_sequence(direction)

        if self.axis == "y":
            time.sleep(self.get_sleep_duration(duration))
            new_direction = direction * -1
            new_position = self.position.get() + new_direction
            self.position.write(new_position)
            self.motor_sequence(new_direction)

    def budge(self, direction):
        self.motor_sequence(direction, 2)

    def go_home(self):
        if self.degree == 0:
            return

        direction = 1
        if self.degree > 0:
            direction = -1

        self.motor_sequence(direction, abs(self.degree))

