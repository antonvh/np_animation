<div align="center">
<img alt="np_animation logo" src="https://raw.githubusercontent.com/antonvh/np_animation/master/img/np_animation.png" width="200">

# np_animation

[![PyPI Version](https://img.shields.io/pypi/v/np_animation.svg)](https://pypi.org/project/np_animation/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![MicroPython](https://img.shields.io/badge/MicroPython-compatible-orange.svg)](https://micropython.org/)

A MicroPython library for driving NeoPixel animations in a tight loop. It works like a mechanism, with time functions and keyframes, making it easy to create complex LED animations for robotics, wearables, and IoT projects.

</div>

This library provides a powerful animation framework that separates animation logic from LED control, allowing you to create smooth, time-based animations with minimal overhead. Perfect for robot lighting effects, indicator lights, and decorative patterns.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Projects & Tutorials](#projects--tutorials)
- [Documentation](#documentation)
- [Supported Platforms](#supported-platforms)
- [License](#license)
- [Author](#author)

## Features

- 🎨 **Rich Animation Functions**: Built-in effects like pulse, hue shift, knight rider, indicators, and brake lights
- ⏱️ **Time-Based Animation**: Smooth animations using time functions and keyframes
- 🎯 **Function Matrix System**: Map multiple animation functions to different LED positions
- 🚗 **Vehicle Lighting**: Ready-made functions for indicators, brake lights, and headlights
- 🌈 **Color Utilities**: HSL/RGB conversion and color manipulation helpers
- 💡 **LED Control**: Direct control over individual LEDs or groups
- 🔄 **Keyframe Animation**: Support for complex keyframe-based animation sequences
- 🎮 **Dynamic Control**: Pass runtime parameters to control animation behavior


## Installation

### On LMS-ESP32

The module should be included in the latest MicroPython firmware from <https://www.antonsmindstorms.com>. If not, use ViperIDE or Thonny and create a new file called `np_animation.py`. Copy the contents from the same file in this repository inside.

### On MicroPython device using `micropip` from PyPI

```python
import micropip
await micropip.install("np_animation")
```

Note: `micropip` must be available on the target board and may require an internet connection from the device.

### Manual Installation

Copy `np_animation.py` to your MicroPython device's filesystem.

## Quick Start

### Basic Animation with Function Matrix

```python
from np_animation import NPAnimation, hue_shift, switch, grb
from time import sleep_ms

# Define animation function matrix
funcs = [
    [[0, 1, 2, 3, 4, 5], hue_shift(period=5000)],  # Rainbow effect on LEDs 0-5
    [[6, 7], switch(on=grb.WHITE, off=grb.OFF, name="headlights")],  # Switchable headlights
]

# Create animation instance (default pin 24, auto-detect LED count)
npa = NPAnimation(funcs)

# Animation loop
try:
    while True:
        npa.update_leds(headlights=True)  # Update with headlights on
        sleep_ms(50)
except KeyboardInterrupt:
    npa.leds_off()
```

### Vehicle Lighting Example

```python
from np_animation import NPAnimation, indicators, brake_lights, switch, grb

# Create a complete vehicle lighting system
funcs = [
    [[0, 1], indicators(name="left_indicators")],   # Left turn signals
    [[10, 11], indicators(name="right_indicators")], # Right turn signals
    [[2, 3], switch(on=grb.WHITE, name="headlights")], # Headlights
    [[8, 9], brake_lights()],  # Brake lights (respond to speed parameter)
]

npa = NPAnimation(funcs, pin=24)

# In your control loop
while True:
    speed = get_motor_speed()  # Your speed function
    npa.update_leds(
        left_indicators=turn_left,
        right_indicators=turn_right,
        headlights=lights_on,
        speed=speed
    )
    sleep_ms(50)
```

### Color Conversion

```python
from np_animation import hsl_to_rgb, rgb_to_hsl, to_grb

# Convert HSL to RGB
rgb = hsl_to_rgb(120, 100, 50)  # Green: (0, 255, 0)

# Convert RGB to HSL
hsl = rgb_to_hsl(255, 0, 0)  # Red: (0, 100, 50)

# Convert RGB to GRB bytes for NeoPixel
grb_bytes = to_grb((255, 0, 0))  # b'\x00\xff\x00'
```

### Knight Rider Effect

```python
from np_animation import NPAnimation, knight_rider, grb

funcs = [
    [[0, 1, 2, 3, 4, 5], knight_rider(period=2000, width=6, color=grb.RED)]
]

npa = NPAnimation(funcs)

while True:
    npa.update_leds()
    sleep_ms(50)
```

### Keyframe Animation

```python
from np_animation import NPAnimation, keyframes, grb

# Define keyframes: (time_ms, [led_colors])
EMERGENCY = [
    (0, [grb.RED]*3 + [grb.OFF]*3),
    (150, [grb.OFF]*6),
    (200, [grb.RED]*3 + [grb.OFF]*3),
    (350, [grb.OFF]*6),
    (500, [grb.OFF]*3 + [grb.BLUE]*3),
    (650, [grb.OFF]*6),
    (1000, [grb.OFF]*6)
]

funcs = [
    [[0, 1, 2, 3, 4, 5], keyframes(EMERGENCY)]
]

npa = NPAnimation(funcs)

while True:
    npa.update_leds()
    sleep_ms(50)
```

## Projects & Tutorials

See np_animation in action! Check out these project tutorials and videos showcasing real-world applications.

### 📝 Blog Tutorials

<table>
<tr>
<td width="50%">
<a href="https://www.antonsmindstorms.com/2024/07/08/creating-a-knight-rider-neopixel-animation-with-python/">
<img src="https://www.antonsmindstorms.com/wp-content/uploads/2024/07/20240707_193241-2048x1153.avif" alt="Knight Rider KITT Scanner" width="100%">
</a>
<h4><a href="https://www.antonsmindstorms.com/2024/07/08/creating-a-knight-rider-neopixel-animation-with-python/">Creating a Knight Rider NeoPixel Animation</a></h4>
<p>Learn how to recreate the iconic KITT scanner effect from the Knight Rider TV series using the knight_rider() function. Includes detailed code explanation and implementation tips.</p>
</td>
<td width="50%">
<a href="https://www.antonsmindstorms.com/2024/08/16/lighting-astro-boy-with-a-radar-sensor-and-rgb-neopixel-leds/">
<img src="https://www.antonsmindstorms.com/wp-content/uploads/2024/07/20240705_213309-2048x1153.avif" alt="Astro Boy with Radar Sensor" width="100%">
</a>
<h4><a href="https://www.antonsmindstorms.com/2024/08/16/lighting-astro-boy-with-a-radar-sensor-and-rgb-neopixel-leds/">Lighting Astro Boy with a Radar Sensor</a></h4>
<p>Add interactive lighting to brick models using a radar proximity sensor. Astro Boy lights up only when someone waves at him, combining multiple animation effects with sensor input.</p>
</td>
</tr>
</table>

### 🎥 Video Tutorials

<table>
<tr>
<td width="50%">
<a href="https://youtu.be/MiwjwRvpz_M">
<img src="https://raw.githubusercontent.com/antonvh/np_animation/master/img/knight_rider_youtube.jpg" alt="Knight Rider Animation Tutorial" width="100%">
</a>
<h4><a href="https://youtu.be/MiwjwRvpz_M">Knight Rider Animation Video Tutorial</a></h4>
<p>Watch the KITT scanner effect in action on a LEGO Technic car with step-by-step implementation guide.</p>
</td>
<td width="50%">
<a href="https://youtu.be/ZBM4gESIHYM">
<img src="https://img.youtube.com/vi/ZBM4gESIHYM/maxresdefault.jpg" alt="Extreme Off-Roader with LED Effects" width="100%">
</a>
<h4><a href="https://youtu.be/ZBM4gESIHYM">Extreme Off-Roader LED Effects</a></h4>
<p>See the np_animation library in full action with complex lighting effects on an off-road vehicle build.</p>
</td>
</tr>
</table>

### 🔗 More Projects

Explore more NeoPixel projects and tutorials on the [NeoPixel tag page](https://www.antonsmindstorms.com/tag/neopixel/) at Anton's Mindstorms.

## Documentation

### Core Class

**`NPAnimation(light_funcs, pin=24, n_leds=0)`**

Main animation class that manages LED updates based on a function matrix.

- `light_funcs`: List of `[led_positions, animation_function]` pairs
- `pin`: GPIO pin for NeoPixel data line
- `n_leds`: Number of LEDs (auto-detected from function matrix if 0)

**Methods:**

- `update_leds(time=None, **kwargs)`: Update all LEDs based on current time and parameters
- `leds_off()`: Turn off all LEDs

### Animation Functions

All animation functions return a function that takes `(time, **kwargs)` and returns color data.

**`hue_shift(period=1000, offset=0)`**  
Continuously shifts through the color spectrum.

**`pulse(color=grb.WHITE, period=5000, offset=0, min_pct=0, max_pct=100)`**  
Pulsing brightness effect with configurable color and range.

**`knight_rider(period=2000, width=6, color=grb.RED)`**  
Classic scanning effect like KITT from Knight Rider.

**`indicators(on=grb.ORANGE, off=grb.OFF, interval=500, name="indicators")`**  
Blinking indicator lights with on/off control.

**`brake_lights(drive=grb.DARK_RED, brake=grb.RED, reverse=grb.WHITE)`**  
Vehicle brake lights that respond to speed parameter.

**`switch(on=grb.WHITE, off=grb.OFF, name="switch")`**  
Simple on/off switch controlled by a boolean parameter.

**`delayed_switch(on=grb.RED, off=grb.OFF, delay=2000)`**  
Switch that turns off after a delay.

**`keyframes(frames)`**  
Play a list of `(time, colors)` keyframes in a loop.

**`keyframes_dict(frames_dict, name="animation")`**  
Switch between multiple keyframe animations at runtime.

### Color Utilities

**`hsl_to_rgb(h, s, l)`** - Convert HSL (0-359, 0-100, 0-100) to RGB (0-255)

**`rgb_to_hsl(r, g, b)`** - Convert RGB to HSL

**`to_grb(rgb)`** - Convert RGB tuple to GRB bytes

**`from_grb(grb)`** - Convert GRB bytes to RGB tuple

### Color Constants

**`grb` class** - Pre-defined colors in GRB byte format:

- `ORANGE`, `BLACK/OFF/NONE`, `WHITE`, `RED`, `DARK_RED`, `BLUE`, `YELLOW`, `GREEN`, `CYAN`, `VIOLET`, `MAGENTA`, `GRAY`

**`rgb` class** - Same colors in RGB tuple format

## Supported Platforms

- **ESP32** with MicroPython
- **LEGO SPIKE Prime/Essential** (with MicroPython firmware)
- **LEGO MINDSTORMS Robot Inventor**
- **Raspberry Pi Pico/Pico W**
- Any MicroPython board with NeoPixel support

## License

MIT License

## Author

Anton Vanhoucke
