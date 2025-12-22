"""
Color Utilities Example

Demonstrates the color conversion utilities in np_animation.
Shows HSL/RGB conversion and how to create custom colors.
"""

from np_animation import hsl_to_rgb, rgb_to_hsl, to_grb, from_grb, grb, rgb

print("=== Color Utilities Demo ===\n")

# Using predefined colors
print("Predefined GRB colors:")
print(f"  Red:    {grb.RED}")
print(f"  Green:  {grb.GREEN}")
print(f"  Blue:   {grb.BLUE}")
print(f"  Orange: {grb.ORANGE}")
print()

print("Predefined RGB colors:")
print(f"  Red:    {rgb.RED}")
print(f"  Green:  {rgb.GREEN}")
print(f"  Blue:   {rgb.BLUE}")
print(f"  Orange: {rgb.ORANGE}")
print()

# HSL to RGB conversion
print("HSL to RGB conversions:")
print(f"  HSL(0, 100, 50) -> RGB{hsl_to_rgb(0, 100, 50)}")  # Red
print(f"  HSL(120, 100, 50) -> RGB{hsl_to_rgb(120, 100, 50)}")  # Green
print(f"  HSL(240, 100, 50) -> RGB{hsl_to_rgb(240, 100, 50)}")  # Blue
print(f"  HSL(30, 100, 50) -> RGB{hsl_to_rgb(30, 100, 50)}")  # Orange
print()

# RGB to HSL conversion
print("RGB to HSL conversions:")
print(f"  RGB(255, 0, 0) -> HSL{rgb_to_hsl(255, 0, 0)}")  # Red
print(f"  RGB(0, 255, 0) -> HSL{rgb_to_hsl(0, 255, 0)}")  # Green
print(f"  RGB(0, 0, 255) -> HSL{rgb_to_hsl(0, 0, 255)}")  # Blue
print(f"  RGB(255, 255, 0) -> HSL{rgb_to_hsl(255, 255, 0)}")  # Yellow
print()

# Converting to GRB bytes for NeoPixel
print("RGB to GRB bytes (for NeoPixel buffer):")
print(f"  RGB(255, 0, 0) -> {to_grb((255, 0, 0))}")
print(f"  RGB(0, 255, 0) -> {to_grb((0, 255, 0))}")
print(f"  RGB(0, 0, 255) -> {to_grb((0, 0, 255))}")
print()

# Converting back from GRB
print("GRB bytes to RGB:")
print(f"  {grb.RED} -> RGB{from_grb(grb.RED)}")
print(f"  {grb.GREEN} -> RGB{from_grb(grb.GREEN)}")
print(f"  {grb.BLUE} -> RGB{from_grb(grb.BLUE)}")
print()

# Creating custom colors using HSL
print("Creating custom colors with HSL:")
for hue in range(0, 360, 60):
    rgb_color = hsl_to_rgb(hue, 100, 50)
    grb_bytes = to_grb(rgb_color)
    print(f"  Hue {hue:3d}° -> RGB{rgb_color} -> GRB{grb_bytes}")
