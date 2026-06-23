# Keyboard listener

Small Python listener that prints to stdout when the following keys are pressed:

- `q`
- `a`
- left arrow
- right arrow

It supports reporting multiple keys pressed simultaneously (e.g. `q + left arrow`).

# Setup:

```bash
python3 -m pip install --user -r requirements.txt
```

# Run the simulator:

```bash
python3 run.py
```

The script prints a line at 10 Hz with the current `speed`, `steering`, and which controls are held. Example:

```
speed=1.00 steering=-30.0 pressed=q+left
```

Press Ctrl-C to exit.
# juniemobile