# np_animation Examples

This directory contains example scripts demonstrating various features of the np_animation library.

## Running Examples

To run any example on your MicroPython device:

1. Copy `np_animation.py` to your device
2. Copy the example file to your device
3. Run the example: `import example_name`

Or use a tool like Thonny, ViperIDE, or ampy to run the scripts directly.

## Available Examples

### basic_rainbow.py

The simplest example showing a rainbow color cycle effect.

- **LEDs required:** 6
- **Features:** `hue_shift()`, basic animation loop

### knight_rider.py

Classic KITT scanner effect from Knight Rider.

- **LEDs required:** 8
- **Features:** `knight_rider()`, smooth scanning animation

### vehicle_lighting.py

Complete vehicle lighting system with headlights, turn signals, and brake lights.

- **LEDs required:** 12
- **Features:** `indicators()`, `brake_lights()`, `switch()`, `pulse()`, multiple animation layers
- **Interactive:** Simulates speed changes and turn signals

### emergency_lights.py

Emergency vehicle lights using keyframe animation.

- **LEDs required:** 6
- **Features:** `keyframes()`, complex timing patterns

### multi_layer.py

Complex multi-layer animation combining multiple effects.

- **LEDs required:** 13

- **Pin:** 24 (default, can be changed in code)
- **LED type:** WS2812B or compatible NeoPixels
- **Power:** Appropriate power supply for your LED count

## Modifying Examples

Each example can be customized by:

- Changing the pin number: `NPAnimation(funcs, pin=YOUR_PIN)`
- Adjusting LED counts: `NPAnimation(funcs, n_leds=YOUR_COUNT)`
- Modifying LED positions in the function matrix
- Adjusting timing parameters (period, interval, etc.)
- Changing colors using the `grb` color constants

## Need Help?

- Check the main [README.md](../README.md) for full API documentation
- Review the inline comments in each example
- Visit <https://github.com/antonvh/np_animation/issues>
Each example can be customized by:
- Changing the pin number: `NPAnimation(funcs, pin=YOUR_PIN)`
- Adjusting LED counts: `NPAnimation(funcs, n_leds=YOUR_COUNT)`
- Modifying LED positions in the function matrix
- Adjusting timing parameters (period, interval, etc.)
- Changing colors using the `grb` color constants
