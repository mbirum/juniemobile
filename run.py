import signal
from sshkeyboard import listen_keyboard
import threading
from motor import Motor
import RPi.GPIO as GPIO
import time


up_pin = 16
down_pin = 18
left_pin = 22
right_pin = 32

wheel_direction = 0
gas = 0

def get_axis_direction_duration(key):
    if key == "left":
        return "x", -1, 0
    elif key == "right":
        return "x", 1, 0
    elif key == "q" or key == "w" or key == "e":
        duration = 1 if key == "q" else 2 if key == "w" else 3
        return "y", -1, duration
    elif key == "1" or key == "2" or key == "3":
        return "y", 1, int(key)
    else:
        return "none", 0, 0

def on_press(key):
    global wheel_direction, gas
    axis, direction, duration = get_axis_direction_duration(key)
    if axis == "x":
        if direction < 0:
            # left
            if wheel_direction > -1:
                wheel_direction = wheel_direction - 1
            if wheel_direction < 0:
                print("left")
                GPIO.output(left_pin, GPIO.HIGH)
                print("--")
            else:
                print("straight")
                GPIO.output(left_pin, GPIO.LOW)
                GPIO.output(right_pin, GPIO.LOW)
        elif direction > 0:
            # right
            if wheel_direction < 1:
                wheel_direction = wheel_direction + 1
            if wheel_direction > 0:
                print("right")
                GPIO.output(right_pin, GPIO.HIGH)
                print("--")
            else:
                print("straight")
                GPIO.output(left_pin, GPIO.LOW)
                GPIO.output(right_pin, GPIO.LOW)
    elif axis == "y":
        if direction < 0:
            # down
            if gas > -1:
                gas = gas - 1
            if gas < 0:
                print("down")
                GPIO.output(down_pin, GPIO.HIGH)
                print("--")
            else:
                print("stop")
                GPIO.output(down_pin, GPIO.LOW)
                GPIO.output(up_pin, GPIO.LOW)
        elif direction > 0:
            # up
            if gas < 1:
                gas = gas + 1
            if gas > 0:
                print("up")
                GPIO.output(up_pin, GPIO.HIGH)
                print("--")
            else:
                print("stop")
                GPIO.output(down_pin, GPIO.LOW)
                GPIO.output(up_pin, GPIO.LOW)


def main():
    print("Where's Junie?")
    print('')
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(up_pin, GPIO.OUT)
    GPIO.output(up_pin, GPIO.LOW)
    GPIO.setup(down_pin, GPIO.OUT)
    GPIO.output(down_pin, GPIO.LOW)
    GPIO.setup(left_pin, GPIO.OUT)
    GPIO.output(left_pin, GPIO.LOW)
    GPIO.setup(right_pin, GPIO.OUT)
    GPIO.output(right_pin, GPIO.LOW)

    def _kb_loop():
        listen_keyboard(on_press=on_press)

    kb_thread = threading.Thread(target=_kb_loop, daemon=True)
    kb_thread.start()
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        print("Exiting.")


if __name__ == '__main__':
    main()

