#!/usr/bin/env python3
"""
Sense HAT joystick reader for PresenceDetector.

Prints "READY" to stdout when ready, then prints:
  - "MIDDLE_PRESS" when the joystick centre/middle button is pressed
  - "MOVE" when the joystick is pressed in up/down/left/right direction
Place this file next to the leshan-client-demo jar (or in the working
directory) when running on a Raspberry Pi with a Sense HAT attached.

Usage (Java invokes this automatically via ProcessBuilder):
    python3 sensehat_joystick.py
"""

import sys

try:
    from sense_hat import SenseHat
except ImportError:
    sys.stderr.write("ERROR: sense_hat module not found. "
                     "Install with: sudo apt-get install sense-hat\n")
    sys.exit(1)

sense = SenseHat()

# Signal to the Java caller that we are ready.
print("READY", flush=True)

while True:
    event = sense.stick.wait_for_event()
    # React to press events only (ignore held/released).
    if event.action != "pressed":
        continue

    if event.direction == "middle":
        print("MIDDLE_PRESS", flush=True)
    elif event.direction in ("up", "down", "left", "right"):
        print("MOVE", flush=True)
