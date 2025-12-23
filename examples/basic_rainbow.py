"""
Basic Rainbow Animation Example

Demonstrates the simplest usage of np_animation with a hue shift effect.
"""

from np_animation import NPAnimation, hue_shift
from time import sleep_ms

# Define animation: LEDs 0-5 will cycle through colors
funcs = [[[0, 1, 2, 3, 4, 5], hue_shift(period=5000)]]

# Create animation instance (pin 21 is used by default for NeoPixel data)
# If you don't pass n_leds, it will be auto-detected from the highest LED index used.
# For example, here we have LEDs 0-5, so n_leds will be set to 6.
npa = NPAnimation(funcs)

print("Starting rainbow animation. Press Ctrl+C to stop.")

try:
    while True:
        npa.update_leds()
        sleep_ms(50)
except KeyboardInterrupt:
    npa.leds_off()
    print("Animation stopped")
