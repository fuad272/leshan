#!/usr/bin/env python3
"""
Sense HAT LED matrix controller for Luminaire.

Prints "READY" to stdout when ready, then reads commands from stdin:
  off             – clear the LED matrix (light off)
  on <dim>        – show the LED matrix at <dim> brightness (0-100)
  heart <dim>     – show a heart at <dim> brightness (0-100)

Place this file next to the leshan-client-demo jar (or in the working
directory) when running on a Raspberry Pi with a Sense HAT attached.

Usage (Java invokes this automatically via ProcessBuilder):
    python3 sensehat_lamp.py
"""

import sys

try:
    from sense_hat import SenseHat
except ImportError:
    sys.stderr.write("ERROR: sense_hat module not found. "
                     "Install with: sudo apt-get install sense-hat\n")
    sys.exit(1)

sense = SenseHat()
sense.clear()

# Signal to the Java caller that we are ready.
print("READY", flush=True)

def set_brightness(dim):
    """Show the full 8x8 matrix at a brightness proportional to dim (0-100)."""
    brightness = max(0, min(255, int(dim * 255 / 100)))
    colour = (brightness, brightness, brightness)
    sense.clear(colour)


def show_heart(dim):
    """Show a heart shape at brightness proportional to dim (0-100)."""
    brightness = max(0, min(255, int(dim * 255 / 100)))
    on = (brightness, 0, 0)
    off = (0, 0, 0)
    pixels = [
        off, on,  on,  off, off, on,  on,  off,
        on,  on,  on,  on,  on,  on,  on,  on,
        on,  on,  on,  on,  on,  on,  on,  on,
        off, on,  on,  on,  on,  on,  on,  off,
        off, off, on,  on,  on,  on,  off, off,
        off, off, off, on,  on,  off, off, off,
        off, off, off, off, off, off, off, off,
        off, off, off, off, off, off, off, off,
    ]
    sense.set_pixels(pixels)


def parse_dim(command):
    try:
        return int(command.split()[1])
    except (IndexError, ValueError):
        return 100

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    if line == "off":
        sense.clear()
    elif line.startswith("on "):
        set_brightness(parse_dim(line))
    elif line.startswith("heart "):
        show_heart(parse_dim(line))
    # Ignore unrecognised commands silently.

# Clean up on stdin close.
sense.clear()
