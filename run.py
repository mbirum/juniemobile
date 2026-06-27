
import sys
import signal
import time
import RPi.GPIO as GPIO
import motor_sequencer
from sshkeyboard import listen_keyboard
import threading

# get axis
if len(sys.argv) < 1:
    print("Usage: python run.py [axis]")
    print("axis: 'x' or 'y'")
    sys.exit(1)
axis = sys.argv[1]

# Motor configuration
updown_pins = [11,13,15,37]
leftright_pins = [16,18,22,36]
control_pins = updown_pins if axis == "y" else leftright_pins
sleep_interval = 0.001
rotation = 30
sequence = motor_sequencer.forward()

# control variables
move_forward = False
move_backward = False
move_left = False
move_right = False
speed = 1

# pin setup
GPIO.setmode(GPIO.BOARD)
if axis == "y":
    for pin in updown_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
elif axis == "x":
    for pin in leftright_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

y_axis_direction = 0
prior_y_direction = 0
x_axis_direction = 0
prior_x_direction = 0


def y_axis_move(direction, speed):
    initial_sequence = motor_sequencer.forward()
    second_sequence = motor_sequencer.backward()
    if direction == "backward":
        initial_sequence = motor_sequencer.backward()
        second_sequence = motor_sequencer.forward()

    # initial sequence
    if direction == "forward":
        print("motor move up")
    elif direction == "backward":
        print("motor move down")
    for i in range(int(rotation)):
        for step in range(len(initial_sequence)):
            y_step = initial_sequence[step % len(initial_sequence)]
            for pin_idx in range(4):
                GPIO.output(updown_pins[pin_idx], y_step[pin_idx])
            time.sleep(sleep_interval)

    if speed == 1:
        time.sleep(0.2)  # Short movement
    elif speed == 2:
        time.sleep(0.6)  # Longer movement for everyday use
    elif speed == 3:
        time.sleep(1.5)  # Only use for long straight-aways

    # second sequence
    if direction == "forward":
        print("motor move down")
    elif direction == "backward":
        print("motor move up")
    for i in range(int(rotation)):
        for step in range(len(second_sequence)):
            y_step = second_sequence[step % len(second_sequence)]
            for pin_idx in range(4):
                GPIO.output(updown_pins[pin_idx], y_step[pin_idx])
            time.sleep(sleep_interval)

    apply_y_direction(0, overwrite=True)  # Reset y_axis_direction after movement

def x_axis_move(direction):
    if direction == "right":
        sequence = motor_sequencer.forward()
    elif direction == "left":
        sequence = motor_sequencer.backward()
    for i in range(int(rotation)):
        for step in range(len(sequence)):
            x_step = sequence[step % len(sequence)]
            # apply x-axis outputs
            for pin_idx in range(4):
                GPIO.output(leftright_pins[pin_idx], x_step[pin_idx])
            time.sleep(sleep_interval)

def apply_x_direction(direction):
    global x_axis_direction
    x_axis_direction = x_axis_direction + direction
    if x_axis_direction > 1:
        x_axis_direction = 1
    elif x_axis_direction < -1:
        x_axis_direction = -1

def apply_y_direction(direction, overwrite=False):
    global y_axis_direction
    if overwrite:
        y_axis_direction = direction
    else:
        y_axis_direction = y_axis_direction + direction
    if y_axis_direction > 1:
        y_axis_direction = 1
    elif y_axis_direction < -1:
        y_axis_direction = -1

def on_press(key):
    global y_axis_direction
    name = key
    if name:
        if name == '1' or name == '2' or name == '3':
            if axis == "y" and y_axis_direction < 1:
                y_axis_move("forward", int(name))
                apply_y_direction(1, overwrite=True)
        elif name == 'q' or name == 'w' or name == 'e':
            translated_speed = 1 if name == 'q' else 2 if name == 'w' else 3
            if axis == "y" and y_axis_direction > -1:
                y_axis_move("backward", translated_speed)
                apply_y_direction(-1, overwrite=True)
        elif name == 'a':
            move_backward = True
        elif name == 'left':
            apply_x_direction(-1)
        elif name == 'right':
            apply_x_direction(1)


def _signal_handler(sig, frame):
    print("\nExiting.")
    sys.exit(0)


def steer():
    global x_axis_direction
    if axis == "x":
        print(f'x-direction={x_axis_direction}')
        if x_axis_direction > prior_x_direction:
            x_axis_move("right")
        elif x_axis_direction < prior_x_direction:
            x_axis_move("left")


TICK = 0.5

def main():
    global x_axis_direction
    signal.signal(signal.SIGINT, _signal_handler)
    print("DRIVE JUNIE, DRIVE!")

    # Run sshkeyboard listener in a daemon thread so the main loop can run.
    def _kb_loop():
        listen_keyboard(on_press=on_press)

    kb_thread = threading.Thread(target=_kb_loop, daemon=True)
    kb_thread.start()

    last_state = None
    try:
        while True:
            steer()
            prior_x_direction = x_axis_direction
            time.sleep(TICK)
    except KeyboardInterrupt:
        pass
    finally:
        # sshkeyboard listener runs in a daemon thread; it will exit with the process.
        print("Exiting.")


if __name__ == '__main__':
    main()

