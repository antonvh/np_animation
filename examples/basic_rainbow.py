"""
Basic Rainbow Animation Example

Demonstrates the simplest usage of np_animation with a hue shift effect.
"""

from np_animation import NPAnimation, hue_shift
from time import sleep_ms

# Define animation: LEDs 0-5 will cycle through colors
funcs = [[[0, 1, 2, 3, 4, 5], hue_shift(period=5000)]]

# Create animation instance (pin 24, auto-detect LED count)
npa = NPAnimation(funcs)

print("Starting rainbow animation. Press Ctrl+C to stop.")

try:
    while True:
        npa.update_leds()
        sleep_ms(50)
except KeyboardInterrupt:
    npa.leds_off()
    print("Animation stopped")
