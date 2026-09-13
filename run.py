import signal
from sshkeyboard import listen_keyboard
import threading
from motor import Motor
import RPi.GPIO as GPIO
import time

# xmotor = Motor("x")
# ymotor = Motor("y")

up_pin = 16
down_pin = 18
left_pin = 22
right_pin = 32

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
    elif key == "o":
        return "x", -1, 2
    elif key == "p":
        return "x", 1, 2
    elif key == "l":
        return "y", -1, 2
    elif key == ";":
        return "y", 1, 2 
    else:
        return "none", 0, 0

def on_press(key):
    axis, direction, duration = get_axis_direction_duration(key)
    if axis == "x":
        if direction < 0:
            # left
            print("left")
            GPIO.output(left_pin, 1)
            time.sleep(1)
            GPIO.output(left_pin, 0)
            print("--")
        elif direction > 0:
            # right
            print("right")
            GPIO.output(right_pin, 1)
            time.sleep(1)
            GPIO.output(right_pin, 0)
            print("--")
    elif axis == "y":
        if direction > 0:
            # up
            print("up")
            GPIO.output(up_pin, 1)
            time.sleep(2)
            GPIO.output(up_pin, 0)
            print("--")
        elif direction < 0:
            # down
            print("down")
            GPIO.output(down_pin, 1)
            time.sleep(1)
            GPIO.output(down_pin, 0)
            print("--")

def main():
    print("DRIVE JUNIE, DRIVE!")
    print('')
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(up_pin, GPIO.OUT)
    GPIO.output(up_pin, 0)
    GPIO.setup(down_pin, GPIO.OUT)
    GPIO.output(down_pin, 0)
    GPIO.setup(left_pin, GPIO.OUT)
    GPIO.output(left_pin, 0)
    GPIO.setup(right_pin, GPIO.OUT)
    GPIO.output(right_pin, 0)

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
        # print('')
        # print("Returning xmotor")
        # xmotor.go_home()
        # print("Returning ymotor")
        # ymotor.go_home()
        GPIO.cleanup()
        print("Exiting.")

if __name__ == '__main__':
    main()

