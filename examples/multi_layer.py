"""
Multi-Layer Animation Example

Demonstrates combining multiple animation effects on different LED groups.
Shows how to create complex lighting systems with independent animations.
"""

from np_animation import NPAnimation, hue_shift, pulse, knight_rider, switch, grb
from time import sleep_ms

# Create a complex multi-layer animation
funcs = [
    # Layer 1: Rainbow shift on first 3 LEDs
    [[0, 1, 2], hue_shift(period=3000)],
    # Layer 2: Pulsing white LEDs in the middle
    [[3, 4], pulse(color=grb.WHITE, period=2000, min_pct=10, max_pct=100)],
    # Layer 3: Knight rider scanner on LEDs 5-10
    [[5, 6, 7, 8, 9, 10], knight_rider(period=1500, width=6, color=grb.CYAN)],
    # Layer 4: Switchable indicator on last LEDs
    [[11, 12], switch(on=grb.ORANGE, off=grb.OFF, name="indicators")],
]

npa = NPAnimation(funcs, pin=24, n_leds=13)

print("Multi-layer animation demo. Press Ctrl+C to stop.")
print("Indicators will blink every 2 seconds")

frame = 0
indicator_state = False

try:
    while True:
        # Toggle indicators every 2 seconds (40 frames at 50ms)
        if frame % 40 == 0:
            indicator_state = not indicator_state

        npa.update_leds(indicators=indicator_state)
        sleep_ms(50)
        frame += 1

except KeyboardInterrupt:
    npa.leds_off()
    print("\nAnimation stopped")
