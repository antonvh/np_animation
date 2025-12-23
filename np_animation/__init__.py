"""
np_animation - A MicroPython library for driving NeoPixel animations

This library provides a powerful animation framework for NeoPixel LEDs,
with time-based functions and keyframes for creating complex lighting effects.
"""

__version__ = "1.1.0"
__author__ = "Antons Mindstorms"
__license__ = "MIT"

from .np_animation import (
    NPAnimation,
    hsl_to_rgb,
    rgb_to_hsl,
    to_grb,
    from_grb,
    grb,
    rgb,
    indicators,
    brake_lights,
    switch,
    delayed_switch,
    hue_shift,
    pulse,
    knight_rider,
    keyframes,
    keyframes_dict,
)

__all__ = [
    "NPAnimation",
    "hsl_to_rgb",
    "rgb_to_hsl",
    "to_grb",
    "from_grb",
    "grb",
    "rgb",
    "indicators",
    "brake_lights",
    "switch",
    "delayed_switch",
    "hue_shift",
    "pulse",
    "knight_rider",
    "keyframes",
    "keyframes_dict",
]
