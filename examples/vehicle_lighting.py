"""
Vehicle Lighting System Example

Demonstrates a complete vehicle lighting setup with:
- Headlights (switchable)
- Turn indicators (left/right)
- Brake lights (speed-responsive)
- Running lights
"""

from np_animation import NPAnimation, indicators, brake_lights, switch, pulse, grb
from time import sleep_ms
import random

# Define LED positions for a typical vehicle setup
# Adjust these numbers based on your actual LED strip layout
funcs = [
    # Front headlights (LEDs 0-1)
    [[0, 1], switch(on=grb.WHITE, off=grb.OFF, name="headlights")],
    # Front running lights with pulse effect (LEDs 2-3)
    [[2, 3], pulse(color=grb.BLUE, period=3000, min_pct=30, max_pct=70)],
    # Left turn indicators (LEDs 4-5)
    [[4, 5], indicators(on=grb.ORANGE, interval=500, name="left_indicators")],
    # Right turn indicators (LEDs 10-11)
    [[10, 11], indicators(on=grb.ORANGE, interval=500, name="right_indicators")],
    # Brake/tail lights (LEDs 8-9)
    [[8, 9], brake_lights(drive=grb.DARK_RED, brake=grb.RED, reverse=grb.WHITE)],
    # Rear running lights (LEDs 6-7)
    [[6, 7], switch(on=grb.DARK_RED, off=grb.OFF, name="running_lights")],
]

# Create animation (assumes 12 LEDs on pin 24)
npa = NPAnimation(funcs, pin=24, n_leds=12)

print("Vehicle lighting demo. Press Ctrl+C to stop.")
print(
    "Simulating: headlights on, running lights on, random indicators and brake lights"
)

# Simulation variables
speed = 0
left_turn = False
right_turn = False
frame = 0

try:
    while True:
        # Simulate speed changes (braking, driving, reversing)
        if frame % 100 == 0:  # Change speed every 5 seconds
            speed = random.choice([0, 30, -20, 50])  # brake, drive, reverse, fast
            print(f"Speed changed to: {speed}")

        # Simulate turn signals
        if frame % 150 == 0:  # Change indicators every 7.5 seconds
            left_turn = random.choice([True, False])
            right_turn = random.choice([True, False]) if not left_turn else False
            print(f"Indicators: left={left_turn}, right={right_turn}")

        # Update all LEDs with current state
        npa.update_leds(
            headlights=True,
            running_lights=True,
            left_indicators=left_turn,
            right_indicators=right_turn,
            speed=speed,
        )

        sleep_ms(50)
        frame += 1

except KeyboardInterrupt:
    npa.leds_off()
    print("\nVehicle lighting stopped")
