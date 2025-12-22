"""
Emergency Lights Keyframe Animation Example

Demonstrates keyframe-based animation for emergency vehicle lights.
"""

from np_animation import NPAnimation, keyframes, grb
from time import sleep_ms

# Define emergency lights pattern
EMERGENCY = [
    (0, [grb.RED] * 3 + [grb.OFF] * 3),
    (150, [grb.OFF] * 6),
    (200, [grb.RED] * 3 + [grb.OFF] * 3),
    (350, [grb.OFF] * 6),
    (400, [grb.RED] * 3 + [grb.OFF] * 3),
    (550, [grb.OFF] * 6),
    (600, [grb.OFF] * 3 + [grb.BLUE] * 3),
    (750, [grb.OFF] * 6),
    (800, [grb.OFF] * 3 + [grb.BLUE] * 3),
    (950, [grb.OFF] * 6),
    (1000, [grb.OFF] * 3 + [grb.BLUE] * 3),
    (1150, [grb.OFF] * 6),
    (1200, [grb.OFF] * 6),  # End of cycle
]

# Create animation with keyframes
funcs = [[[0, 1, 2, 3, 4, 5], keyframes(EMERGENCY)]]

npa = NPAnimation(funcs, pin=24, n_leds=6)

print("Emergency lights animation. Press Ctrl+C to stop.")

try:
    while True:
        npa.update_leds()
        sleep_ms(50)
except KeyboardInterrupt:
    npa.leds_off()
    print("Emergency lights stopped")
