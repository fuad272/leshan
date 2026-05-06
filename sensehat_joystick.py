#!/usr/bin/env python3
"""
Sense HAT joystick reader for PresenceDetector.

Prints "READY" to stdout when ready, then prints "PRESS" each time the
joystick middle (center) button is pressed.  Place this file next to the
leshan-client-demo jar (or in the working directory) when running on a
Raspberry Pi with a Sense HAT attached.

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
    # Only react to the centre/middle button being pressed (not held/released).
    if event.direction == "middle" and event.action == "pressed":
        print("PRESS", flush=True)
