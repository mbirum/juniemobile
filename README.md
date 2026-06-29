# JunieMobile

JunieMobile is a small Python project for controlling motors and running simple motor sequences. It provides a lightweight set of scripts and modules to drive motors (via `motor.py`) and orchestrate timed sequences (`motor_sequencer.py`). This README explains how to install, run, and extend the project.

**Contents**
- **Purpose:** Quick local tooling for motor control and sequencing for development and testing.
- **Language:** Python 3.8+
- **Repository files:** See the Files section for a quick map.

**Quick Start**

1. Install dependencies:

```bash
python3 -m pip install --user -r requirements.txt
```

2. Run the main script (example):

```bash
python3 run.py
# or use the shell wrapper
./run.sh
```

3. For hardware/deployment actions there is `push.sh` which performs project-specific push steps (make sure it is executable):

```bash
chmod +x push.sh
./push.sh
```

## Files
- `run.py` - Project entrypoint / demo runner. Runs a simple sequence or example flow.
- `run.sh` - Simple shell wrapper to launch `run.py` using the appropriate Python environment.
- `motor.py` - Motor control module. Contains the `Motor` class and low-level motor operations.
- `motor_sequencer.py` - Sequencer to run predefined motor movement sequences and timing.
- `push.sh` - Helper script for pushing or deploying the project (project-specific).
- `requirements.txt` - Python dependencies for the project.

## Requirements
- Python 3.8 or newer.
- Dependencies listed in `requirements.txt` (install with pip).
- If you are using physical motor hardware, ensure the host has required access rights to serial/USB devices and any required hardware drivers.

## Usage

- Running the sequencer directly:

```bash
python3 motor_sequencer.py
```

- Importing `Motor` in your own script:

```python
from motor import Motor

# example usage
motor = Motor(port='/dev/ttyUSB0')
motor.connect()
motor.move(steps=100, speed=50)
motor.disconnect()
```

## Notes and Tips
- Serial/USB permissions (macOS): you may need to grant Terminal access to the USB device or run scripts with appropriate privileges.
- Virtual environments: creating a venv is recommended:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Development
- To extend the sequencer, edit `motor_sequencer.py` and add sequence steps. Keep motor-safe limits in mind.
- Follow the style in existing files; avoid changing public APIs for `Motor` unless necessary.

## Troubleshooting
- If imports fail, ensure you installed dependencies into the same Python environment used to run commands.
- If the motor does not respond, verify the physical connection and device port, and check logs printed by `motor.py`.

## Contributing
- Open an issue describing the change or bug you want to address.
- Fork the repo, create a branch, and submit a pull request.

## License
- This repository does not include a license file. Add one if you intend to publish or distribute.

## Contact
- For questions or help, open an issue in the repository.

---

If you'd like, I can also:
- add a minimal example script that runs a safe demo sequence,
- add a `requirements.txt` review, or
- create a tiny test harness to verify `motor.py` functions.
