
"""Simulator-style keyboard input for a simple car model.

Controls:
- `q` held: move forward
- `a` held: move backward
- `left arrow` held: steer left
- `right arrow` held: steer right

The script maintains a set of currently-pressed controls and runs a fixed-rate
simulation loop, publishing `speed` and `steering` each tick. Holding a key
produces continuous control; releasing it returns the control to zero.
"""

import sys
import signal
import time
import RPi.GPIO as GPIO
import motor_sequencer
from sshkeyboard import listen_keyboard
import threading

# Motor configuration
updown_pins = [11,13,15,37]
leftright_pins = [16,18,22,36]
sleep_interval = 0.001
rotation = 30
sequence = motor_sequencer.forward()

moving_forward = False
moving_backward = False
moving_left = False
moving_right = False

GPIO.setmode(GPIO.BOARD)
for pin in updown_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
for pin in leftright_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)

y_axis_direction = 0
x_axis_direction = 0

# canonical target names used internally
TARGET_KEYS = {
    'q': 'q',
    'a': 'a',
    'left': 'left',
    'right': 'right',
    'LEFT': 'left',
    'RIGHT': 'right',
}

# set of currently held target names (subset of {'q','a','left','right'})
pressed = set()

# simulator parameters
TICK = 0.01  # seconds between updates (10 Hz)
MAX_SPEED = 1.0  # m/s for forward/backward when held
STEER_ANGLE = 30.0  # degrees left/right when held


def _name_from_key(key):
    # sshkeyboard passes simple strings for keys (e.g. 'q', 'left', 'RIGHT')
    if isinstance(key, str):
        k = key.lower()
        if k in ('left', 'arrow_left', 'left_arrow', '←'):
            return 'left'
        if k in ('right', 'arrow_right', 'right_arrow', '→'):
            return 'right'
        if k in ('q', 'a'):
            return k
        return None
    # fallback for objects (compat with pynput-like keys)
    try:
        char = key.char
    except AttributeError:
        return None
    if char is None:
        return None
    return TARGET_KEYS.get(char.lower())

def y_axis_move(direction):
    if direction == "forward":
        sequence = motor_sequencer.forward()
    elif direction == "backward":
        sequence = motor_sequencer.backward()
    for i in range(int(rotation)):
        for step in range(len(sequence)):
            y_step = sequence[step % len(sequence)]
            # apply y-axis outputs
            for pin_idx in range(4):
                GPIO.output(updown_pins[pin_idx], y_step[pin_idx])
            time.sleep(sleep_interval)

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

def on_press(key):
    name = _name_from_key(key)
    if name:
        if name not in pressed:
            pressed.add(name)
            if name == 'q':
                print("Moving forward")
                y_axis_move("forward")
            elif name == 'a':
                print("Moving backward")
                y_axis_move("backward")
            elif name == 'left':
                print("Steering left")
                x_axis_move("left")
            elif name == 'right':
                print("Steering right")
                x_axis_move("right")

def on_release(key):
    name = _name_from_key(key)
    if name and name in pressed:
        pressed.remove(name)
        if name == 'q':
            print("Stopped moving forward")
            y_axis_move("backward")
        elif name == 'a':
            print("Stopped moving backward")
            y_axis_move("forward")
        elif name == 'left':
            print("Stopped steering left")
            x_axis_move("right")
        elif name == 'right':
            print("Stopped steering right")
            x_axis_move("left")


def _signal_handler(sig, frame):
    print("\nExiting.")
    sys.exit(0)


def compute_controls(held):
    """Return (speed, steering) based on currently held controls.

    speed: positive forward, negative backward, zero if neither or both.
    steering: negative = left degrees, positive = right degrees, zero if neither or both.
    """
    global y_axis_direction, x_axis_direction

    forward = 'q' in held
    backward = 'a' in held
    left = 'left' in held
    right = 'right' in held

    if forward and not backward:
        speed = MAX_SPEED
        y_axis_direction = 1
    elif backward and not forward:
        speed = -MAX_SPEED
        y_axis_direction = -1
    else:
        speed = 0.0
        y_axis_direction = 0

    if left and not right:
        steering = -STEER_ANGLE
        x_axis_direction = -1
    elif right and not left:
        steering = STEER_ANGLE
        x_axis_direction = 1
    else:
        steering = 0.0
        x_axis_direction = 0
    return speed, steering


def drive():
    """Step both motors so x and y can move simultaneously.

    Each axis uses the same 4-step sequence from `motor_sequencer`. When an
    axis is idle its outputs are driven low. Sequences are stepped in
    lockstep so both axes can move together.
    """
    global y_axis_direction, x_axis_direction

    # choose sequences per-axis (idle -> single all-zero step)
    if y_axis_direction > 0:
        y_seq = motor_sequencer.forward()
    elif y_axis_direction < 0:
        y_seq = motor_sequencer.backward()
    else:
        y_seq = [[0, 0, 0, 0]]

    if x_axis_direction > 0:
        x_seq = motor_sequencer.forward()
    elif x_axis_direction < 0:
        x_seq = motor_sequencer.backward()
    else:
        x_seq = [[0, 0, 0, 0]]

    # step both sequences together
    max_steps = max(len(y_seq), len(x_seq))
    for i in range(int(rotation)):
        for step in range(max_steps):
            y_step = y_seq[step % len(y_seq)]
            x_step = x_seq[step % len(x_seq)]

            # apply y-axis outputs
            for pin_idx in range(4):
                GPIO.output(updown_pins[pin_idx], y_step[pin_idx])

            # apply x-axis outputs
            for pin_idx in range(4):
                GPIO.output(leftright_pins[pin_idx], x_step[pin_idx])

            time.sleep(sleep_interval)


def main():
    signal.signal(signal.SIGINT, _signal_handler)
    print("Simulator listening — hold keys to control the car. Ctrl-C to exit.")
    print("Controls: q=forward, a=back, ←=left, →=right")

    # Run sshkeyboard listener in a daemon thread so the main loop can run.
    def _kb_loop():
        listen_keyboard(on_press=on_press, on_release=on_release)

    kb_thread = threading.Thread(target=_kb_loop, daemon=True)
    kb_thread.start()

    last_state = None
    try:
        while True:
            do_nothing = True
            # speed, steering = compute_controls(pressed)
            # state = (speed, steering, tuple(sorted(pressed)))
            # print every tick; if you prefer only on-change, compare with last_state
            # print(f"speed={speed:.2f} steering={steering:.1f} pressed={'+'.join(sorted(pressed)) or 'none'}")
            # sys.stdout.flush()
            # last_state = state
            time.sleep(TICK)
    except KeyboardInterrupt:
        pass
    finally:
        # sshkeyboard listener runs in a daemon thread; it will exit with the process.
        print("Exiting.")


if __name__ == '__main__':
    main()

