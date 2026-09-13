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
    global wheel_direction
    axis, direction, duration = get_axis_direction_duration(key)
    if axis == "x":
        if direction < 0:
            # left
            if wheel_direction > -1:
                wheel_direction = wheel_direction - 1
                print(f"wheel_direction: {wheel_direction}")
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
                print(f"wheel_direction: {wheel_direction}")
            if wheel_direction > 0:
                print("right")
                GPIO.output(right_pin, GPIO.HIGH)
                print("--")
            else:
                print("straight")
                GPIO.output(left_pin, GPIO.LOW)
                GPIO.output(right_pin, GPIO.LOW)
    elif axis == "y":
        if direction > 0:
            print("forward")
            GPIO.output(up_pin, GPIO.HIGH)
            if duration == 1:
                time.sleep(0.1)
            elif duration == 2:
                time.sleep(0.35)
            elif duration == 3:
                time.sleep(0.75)
            GPIO.output(up_pin, GPIO.LOW)
            print("--")
        elif direction < 0:
            print("back")
            GPIO.output(down_pin, GPIO.HIGH)
            if duration == 1:
                time.sleep(0.1)
            elif duration == 2:
                time.sleep(0.35)
            elif duration == 3:
                time.sleep(0.75)
            GPIO.output(down_pin, GPIO.LOW)
            print("--")

def on_release(key):
    print(f"Key released: {key}")

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
        listen_keyboard(on_press=on_press, on_release=on_release, delay_second_char=0.01, delay_other_char=0.01)
        
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

