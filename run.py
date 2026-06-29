import signal
from sshkeyboard import listen_keyboard
import threading
from motor import Motor

xmotor = Motor("x")
ymotor = Motor("y")

TICK = 0.01

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
    axis, direction, duration = get_axis_direction_duration(key)
    print(f'\{{axis}\} \{{direction}\} \{{duration}\}')
    if axis == "x":
        if xmotor.free():
            xmotor.move(direction, duration)
    elif axis == "y":
        if ymotor.free():
            ymotor.move(direction, duration)

def main():
    print("DRIVE JUNIE, DRIVE!")
    # Run sshkeyboard listener in a daemon thread so the main loop can run.
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
        print("Returning xmotor")
        xmotor.go_home()
        print("Returning ymotor")
        ymotor.go_home()
        print("Exiting.")

if __name__ == '__main__':
    main()

