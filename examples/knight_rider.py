"""
Knight Rider Scanner Effect Example

Creates the classic KITT scanner effect from Knight Rider.
"""

from np_animation import NPAnimation, knight_rider, grb
from time import sleep_ms

# Create a scanner effect on LEDs 0-7
funcs = [[[0, 1, 2, 3, 4, 5, 6, 7], knight_rider(period=2000, width=8, color=grb.RED)]]

# Create animation instance
npa = NPAnimation(funcs, pin=24, n_leds=8)

print("Knight Rider scanner effect. Press Ctrl+C to stop.")

try:
    while True:
        npa.update_leds()
        sleep_ms(50)
except KeyboardInterrupt:
    npa.leds_off()
    print("Scanner stopped")
