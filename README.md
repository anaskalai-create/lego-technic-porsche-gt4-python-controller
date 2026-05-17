# LEGO Technic Bluetooth Controller

Python project for controlling a LEGO Technic Move Hub via Bluetooth with an Xbox controller.

The project connects real hardware with software: controller input is read with `pygame`, processed in Python and sent to the LEGO Technic Move Hub via Bluetooth Low Energy using `bleak`.

## Features

- Bluetooth Low Energy connection to LEGO Technic Move Hub
- Xbox controller input with `pygame`
- Forward and reverse throttle control
- Steering control with dead-zone handling
- Brake mode with controller rumble feedback
- Light toggle and braking light mode
- Object-oriented Python structure
- Asynchronous BLE communication with `asyncio`

## Tech Stack

- Python
- asyncio
- bleak
- pygame
- Bluetooth Low Energy
- Object-Oriented Programming

## Project Structure

```text
lego-technic-python-controller/
├── main.py
├── util/
│   ├── __init__.py
│   ├── TechnicMoveHub.py
│   └── XboxController.py
├── docs/
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Connect the Xbox controller to the computer.
2. Turn on the LEGO Technic Move Hub.
3. Start the program:

```bash
python main.py
```

## Controls

| Input | Action |
|---|---|
| Right trigger | Drive forward |
| Left trigger | Reverse |
| Left stick horizontal | Steering |
| RB button | Brake |
| A button | Toggle lights |
| Select button | Exit program |

## Code Overview

### `main.py`

Contains the `Porsche` class. It connects the controller with the LEGO hub and runs the main control loop.

### `util/TechnicMoveHub.py`

Handles Bluetooth scanning, connecting, pairing, calibration and sending motor commands to the hub.

### `util/XboxController.py`

Handles Xbox controller initialization and reads throttle, steering, brake, light and exit input.

## Notes

This project requires compatible Bluetooth hardware and a LEGO Technic Move Hub. Button mappings can differ depending on controller model, operating system and driver.

## Demo

Add a short video or GIF in the `docs/` folder to show the controller and LEGO model in action.
