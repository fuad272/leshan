#!/usr/bin/env python3
"""
Sense HAT display helper for PresenceDetector motion mode.

Usage:
    python3 sensehat_display.py heart
    python3 sensehat_display.py clear
"""

import sys

try:
    from sense_hat import SenseHat
except ImportError:
    sys.stderr.write("ERROR: sense_hat module not found. "
                     "Install with: sudo apt-get install sense-hat\n")
    sys.exit(1)

if len(sys.argv) < 2:
    sys.exit(2)

command = sys.argv[1].lower()
sense = SenseHat()

if command == "heart":
    red = (255, 0, 0)
    off = (0, 0, 0)
    heart = [
        off, red, red, off, off, red, red, off,
        red, red, red, red, red, red, red, red,
        red, red, red, red, red, red, red, red,
        off, red, red, red, red, red, red, off,
        off, off, red, red, red, red, off, off,
        off, off, off, red, red, off, off, off,
        off, off, off, off, off, off, off, off,
        off, off, off, off, off, off, off, off,
    ]
    sense.set_pixels(heart)
elif command == "clear":
    sense.clear()
