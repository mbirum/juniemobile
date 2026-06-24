
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
from pynput import keyboard

# Motor configuration
updown_pins = [0,2,3,25]
leftright_pins = [4,5,6,27]
sleep_interval = 0.001
rotation = 20
sequence = motor_sequencer.forward()

for pin in updown_pins + leftright_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)

y_axis_direction = 0
x_axis_direction = 0

# canonical target names used internally
TARGET_KEYS = {
    'q': 'q',
    'a': 'a',
    keyboard.Key.left: 'left',
    keyboard.Key.right: 'right',
}

# set of currently held target names (subset of {'q','a','left','right'})
pressed = set()

# simulator parameters
TICK = 0.1  # seconds between updates (10 Hz)
MAX_SPEED = 1.0  # m/s for forward/backward when held
STEER_ANGLE = 30.0  # degrees left/right when held


def _name_from_key(key):
    if key in (keyboard.Key.left, keyboard.Key.right):
        return TARGET_KEYS.get(key)
    try:
        char = key.char
    except AttributeError:
        return None
    if char is None:
        return None
    return TARGET_KEYS.get(char.lower())


def on_press(key):
    name = _name_from_key(key)
    if name:
        pressed.add(name)


def on_release(key):
    name = _name_from_key(key)
    if name and name in pressed:
        pressed.remove(name)


def _signal_handler(sig, frame):
    print("\nExiting.")
    sys.exit(0)


def compute_controls(held):
    """Return (speed, steering) based on currently held controls.

    speed: positive forward, negative backward, zero if neither or both.
    steering: negative = left degrees, positive = right degrees, zero if neither or both.
    """
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
    if y_axis_direction < 0:
        sequence = motor_seq.getForwardSequence()
        for i in range(int(rotation)):
            for step in range(len(sequence)):
                for pin in range(4):
                    GPIO.output(control_pins[pin], sequence[step][pin])
                time.sleep(sleep_interval)
    elif y_axis_direction > 0:
        sequence = motor_seq.getBackwardSequence()
        for i in range(int(rotation)):
            for step in range(len(sequence)):
                for pin in range(4):
                    GPIO.output(control_pins[pin], sequence[step][pin])
                time.sleep(sleep_interval)


def main():
    signal.signal(signal.SIGINT, _signal_handler)
    print("Simulator listening — hold keys to control the car. Ctrl-C to exit.")
    print("Controls: q=forward, a=back, ←=left, →=right")

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    last_state = None
    try:
        while True:
            speed, steering = compute_controls(pressed)
            drive()
            state = (speed, steering, tuple(sorted(pressed)))
            # print every tick; if you prefer only on-change, compare with last_state
            print(f"speed={speed:.2f} steering={steering:.1f} pressed={'+'.join(sorted(pressed)) or 'none'}")
            sys.stdout.flush()
            last_state = state
            time.sleep(TICK)
    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
        print("Exiting.")


if __name__ == '__main__':
    main()

