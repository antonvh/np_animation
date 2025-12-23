# This library is handy for driving neopixel animations in a tight loop
# It works much like a mechanism, with time functions and keyframes.

from neopixel import NeoPixel
from machine import Pin
import utime
from math import pi, sin


def __clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


def __scale(val, src, dst):
    ## Returns the given value scaled from the scale of src to the scale of dst.
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]


def __saturate(value):
    return __clamp(value, 0.0, 1.0)


def __hue_to_rgb(h):
    r = abs(h * 6.0 - 3.0) - 1.0
    g = 2.0 - abs(h * 6.0 - 2.0)
    b = 2.0 - abs(h * 6.0 - 4.0)
    return __saturate(r), __saturate(g), __saturate(b)


def hsl_to_rgb(h, s, l):
    """Turns h, s and l values into an rgb tuple

    Args:
        h (int/float): hue in range 0-359
        s (int/float): saturation in range 0-99
        l (int/float): lightness in range 0-99

    Returns:
        tuple: (r,g,b) in range 0-255
    """
    # Use explicit float division for better precision
    h = h / 359.0
    s = s / 100.0
    l = l / 100.0
    r, g, b = __hue_to_rgb(h)
    c = (1.0 - abs(2.0 * l - 1.0)) * s
    r = (r - 0.5) * c + l
    g = (g - 0.5) * c + l
    b = (b - 0.5) * c + l
    # Clamp and round to prevent out-of-range values
    rgb = tuple([max(0, min(255, round(x * 255))) for x in (r, g, b)])
    return rgb


def rgb_to_hsl(r, g, b):
    """Converts the values r,g and b into a hsl tuple

    Args:
        r (int): red
        g (int): green
        b (int): blue

    Returns:
        tuple: (h,s,l) with h in range 0-359, s & l in range 0-100
    """
    # Use explicit float division for better precision
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0
    high = max(r, g, b)
    low = min(r, g, b)
    h, s, l = ((high + low) / 2.0,) * 3

    if high == low:
        h = 0.0
        s = 0.0
    else:
        d = high - low
        s = d / (2.0 - high - low) if l > 0.5 else d / (high + low)
        h = {
            r: (g - b) / d + (6.0 if g < b else 0.0),
            g: (b - r) / d + 2.0,
            b: (r - g) / d + 4.0,
        }[high]
        h /= 6.0

    # Convert to degrees and normalize to 0-359 range
    h_deg = h * 360.0
    if h_deg >= 360.0:
        h_deg = 0.0

    return round(h_deg), round(s * 100.0), round(l * 100.0)


def to_grb(rgb):
    """Convert an (r,g,b) tuple into grb bytes for neopixel buffer

    Args:
        rgb (tuple): (r,g,b)

    Returns:
        bytes: grb values
    """
    return bytes((rgb[1], rgb[0], rgb[2]))


def from_grb(grb):
    """Convert 3 bytes of grb into a an rgb tuple

    Args:
        grb (bytes): grb buffer bytes

    Returns:
        tuple: (r,g,b)
    """
    return grb[1], grb[0], grb[2]


class grb:
    """Enumerator class for GRB byte colors (NeoPixel format).

    Provides predefined color constants as 3-byte sequences in GRB format
    (Green, Red, Blue) which is the native format for NeoPixel LEDs.

    Attributes:
        ORANGE: Orange color
        BLACK/NONE/OFF: Black/off (all are aliases)
        WHITE: White color
        RED: Red color
        DARK_RED: Dark red color
        BLUE: Blue color
        YELLOW: Yellow color
        GREEN: Green color
        CYAN: Cyan color
        VIOLET: Violet color
        MAGENTA: Magenta color
        GRAY: Gray color
    """

    ORANGE = b"\x66\xfc\x03"
    BLACK = NONE = OFF = b"\x00\x00\x00"
    WHITE = b"\xff\xff\xff"
    RED = b"\x00\xff\x00"
    DARK_RED = b"\x00\x44\x00"
    BLUE = b"\x00\x00\xff"
    YELLOW = b"\xff\xff\x00"  # (255,255,0),
    GREEN = b"\xff\x00\x00"  # (0,255,0),
    CYAN = b"\xff\x00\xff"  #: (0,255,255),
    VIOLET = b"\x7f\x7f\xff"  #: (127,127,255),
    MAGENTA = b"\x00\xff\xff"  #: (255,0,255),
    GRAY = b"\x7f\x7f\x7f"  #: (127,127,127),


class rgb:
    """Enumerator class for RGB tuples.

    Provides predefined color constants as (r, g, b) tuples with values 0-255.
    These correspond to the same colors in the grb class but in standard RGB format.

    Attributes:
        ORANGE: Orange color tuple
        BLACK/NONE/OFF: Black/off (all are aliases)
        WHITE: White color tuple
        RED: Red color tuple
        DARK_RED: Dark red color tuple
        BLUE: Blue color tuple
        YELLOW: Yellow color tuple
        GREEN: Green color tuple
        CYAN: Cyan color tuple
        VIOLET: Violet color tuple
        MAGENTA: Magenta color tuple
        GRAY: Gray color tuple
    """

    ORANGE = from_grb(grb.ORANGE)
    BLACK = NONE = OFF = from_grb(grb.BLACK)
    WHITE = from_grb(grb.WHITE)
    RED = from_grb(grb.RED)
    DARK_RED = from_grb(grb.DARK_RED)
    BLUE = from_grb(grb.BLUE)
    YELLOW = from_grb(grb.YELLOW)
    GREEN = from_grb(grb.GREEN)
    CYAN = from_grb(grb.CYAN)
    VIOLET = from_grb(grb.VIOLET)
    MAGENTA = from_grb(grb.MAGENTA)
    GRAY = from_grb(grb.GRAY)


def indicators(on=grb.ORANGE, off=grb.OFF, interval=500, name="indicators"):
    """Create blinking indicator lights (like turn signals).

    Returns a function that can be assigned to LEDs in an animation loop.
    This function is for use in a function matrix for an NPAnimation() object.

    Args:
        on (bytes, optional): GRB byte color when indicator is on. Defaults to grb.ORANGE.
        off (bytes, optional): GRB byte color when indicator is off. Defaults to grb.OFF.
        interval (int, optional): Time on and off in milliseconds. Defaults to 500.
        name (str, optional): Keyword argument name for the on/off switch. Defaults to "indicators".

    Returns:
        function: Animation function func(time, **kwargs) that returns 3 GRB bytes.
    """

    def func(time, **kwargs):
        switch = True
        if name in kwargs:
            switch = kwargs[name]
        return on if (time % (interval * 2) < interval) and switch else off

    return func


def indicators_right(on=grb.ORANGE, off=grb.OFF, interval=500):
    """Deprecated"""

    def func(time, turn=0, **kwargs):
        return on if (time % (interval * 2) < interval) and turn > 0 else off

    return func


def brake_lights(drive=grb.DARK_RED, brake=grb.RED, reverse=grb.WHITE):
    """Create speed-responsive brake/tail lights.

    Returns a function that returns 3 GRB bytes depending on the value of speed.
    This function is for use in a function matrix for an NPAnimation() object.

    Args:
        drive (bytes, optional): Color when speed > 0 (driving). Defaults to grb.DARK_RED.
        brake (bytes, optional): Color when speed == 0 (braking). Defaults to grb.RED.
        reverse (bytes, optional): Color when speed < 0 (reversing). Defaults to grb.WHITE.

    Returns:
        function: Animation function func(time, speed=0, **kwargs) that returns 3 GRB bytes.
    """

    def func(time, speed=0, **kwargs):
        if speed < 0:
            return reverse
        elif speed > 0:
            return drive
        else:
            return brake

    return func


def switch(on=grb.WHITE, off=grb.OFF, name="switch"):
    """Create a simple on/off switch for LEDs.

    Generates a function that returns one of two GRB byte colors depending on a boolean switch.
    This function is for use in a function matrix for an NPAnimation() object.

    Args:
        on (bytes, optional): Color when switch is True. Defaults to grb.WHITE.
        off (bytes, optional): Color when switch is False. Defaults to grb.OFF.
        name (str, optional): Keyword argument name for the switch. Defaults to "switch".

    Returns:
        function: Animation function func(time, **kwargs) that returns 3 GRB bytes.
    """

    def func(time, **kwargs):
        switch = True
        if name in kwargs:
            switch = kwargs[name]
        return on if switch else off

    return func


def delayed_switch(on=grb.RED, off=grb.OFF, delay=2000):
    """Create a timed switch that turns off after a delay.

    Generates a function that returns one of two GRB byte colors depending on whether
    a timer has expired. This function is for use in a function matrix for an NPAnimation() object.

    Args:
        on (bytes, optional): Color while timer is running. Defaults to grb.RED.
        off (bytes, optional): Color after timer expires. Defaults to grb.OFF.
        delay (int, optional): Timer duration in milliseconds. Defaults to 2000.

    Returns:
        function: Animation function func(time, **kwargs) that returns 3 GRB bytes.
    """

    def func(time, **kwargs):
        return on if time < delay else off

    return func


def hue_shift(period=1000, offset=0):
    """Create a rainbow color cycling effect.

    Generates a function that returns continuously shifting GRB byte colors through
    the full hue spectrum. This function is for use in a function matrix for an NPAnimation() object.

    Args:
        period (int, optional): Duration of one full color cycle in milliseconds. Defaults to 1000.
        offset (int, optional): Time offset for phase shifting. Defaults to 0.

    Returns:
        function: Animation function func(time, **kwargs) that returns 3 GRB bytes.
    """

    def func(time, **kwargs):
        hsl = (
            ((time + offset) % period) / period * 360,
            100,  # Full saturation
            50,  # Half lightness
        )
        return to_grb(hsl_to_rgb(*hsl))

    return func


def pulse(color=grb.WHITE, period=5000, offset=0, min_pct=0, max_pct=100):
    """Create a pulsing/breathing light effect.

    Generates a function that returns a smoothly pulsing GRB byte color using a sine wave.
    This function is for use in a function matrix for an NPAnimation() object.

    Args:
        color (bytes, optional): Base color to pulse. Defaults to grb.WHITE.
        period (int, optional): Duration of one complete pulse cycle in milliseconds. Defaults to 5000.
        offset (int, optional): Time offset for phase calculation. Defaults to 0.
        min_pct (int, optional): Minimum brightness percentage (0-100). Defaults to 0.
        max_pct (int, optional): Maximum brightness percentage (0-100). Defaults to 100.

    Returns:
        function: Animation function func(time, **kwargs) that returns 3 GRB bytes.
    """

    def func(time, **kwargs):
        # Make b vary between 0.0 and 1.0 within the period
        b = __scale(
            sin((time + offset) * 2 * pi / period),
            (-1, 1),
            (min_pct / 100, max_pct / 100),
        )
        return bytes([int(b * c) for c in color])

    return func


def rotate(l, n):
    return l[-n:] + l[:-n]


def knight_rider(period=2000, width=6, color=grb.RED):
    """Create a Knight Rider scanner effect.

    Generates a function that returns a list of GRB bytes creating a sweeping
    scanner effect like the iconic Knight Rider car.
    This function is for use in a function matrix for an NPAnimation() object.

    Args:
        period (int, optional): Duration of one complete sweep cycle in milliseconds. Defaults to 2000.
        width (int, optional): Number of LEDs in the scanner effect. Defaults to 6.
        color (bytes, optional): Base color of the scanner. Defaults to grb.RED.

    Returns:
        function: Animation function func(time, **kwargs) that returns a list of width GRB byte sequences.
    """

    def b(n, center):
        # Brightness function, gauss-like with a max of 1 around center
        return 2 ** (-1.5 / width * (n - center) ** 2)

    def func(time, **kwargs):
        # Bounce the center from left to right with a sine function
        center = 0.5 * (sin(time * 2 * pi / period) + 1) * width
        # Return brightness adjusted color for each led.
        return [bytes([int(b(n, center) * c) for c in color]) for n in range(width)]

    return func


def knight_rider_gen(period=2000, width=6):
    """Generator function for Knight Rider scanner animation.

    Yields keyframes for a Knight Rider style scanner effect.

    Args:
        period (int, optional): Duration of one complete sweep in milliseconds. Defaults to 2000.
        width (int, optional): Number of LEDs in the effect. Defaults to 6.

    Yields:
        tuple: (time_ms, list) containing timestamp and list of GRB byte sequences.
    """
    stepsize = int(255 / (width - 1))
    strip = [0] * width + list(range(0, 256, stepsize))
    r_strip = strip[:]
    r_strip.reverse()
    n = 0
    while n <= 2 * width:
        result = [grb.OFF] * width
        for i in range(width):
            result[i] = bytes((0, max(rotate(strip, n)[i], rotate(r_strip, -n)[i]), 0))
        yield int(period / (2 * width) * n), result
        n += 1


EMERGENCY_1 = [
    (0, [grb.RED] * 3 + [grb.OFF] * 3),
    (150, [grb.OFF] * 6),
    (200, [grb.RED] * 3 + [grb.OFF] * 3),
    (350, [grb.OFF] * 6),
    (400, [grb.RED] * 3 + [grb.OFF] * 3),
    (450, [grb.OFF] * 6),
    (500, [grb.OFF] * 3 + [grb.BLUE] * 3),
    (650, [grb.OFF] * 6),
    (700, [grb.OFF] * 3 + [grb.BLUE] * 3),
    (850, [grb.OFF] * 6),
    (900, [grb.OFF] * 3 + [grb.BLUE] * 3),
    (1050, [grb.OFF] * 6),
    (1100, [grb.OFF] * 6),
]


def keyframes(frames):
    """Create animation from a keyframe list.

    Generates a function that returns GRB bytes based on keyframe timing.
    Looks up the appropriate keyframe based on the current time.
    This function is for use in a function matrix for an NPAnimation() object.

    Args:
        frames (list): List of (time_ms, pixels) tuples where time_ms is the timestamp
            in milliseconds and pixels is a list of GRB byte sequences.

    Returns:
        function: Animation function func(time, **kwargs) that returns GRB bytes or list of GRB bytes.
    """
    frames.reverse()
    period = frames[0][0]
    if period == 0:
        period = 1

    def func(time, **kwargs):
        result = [grb.OFF]
        for frame_time, pixels in frames:
            if time % period >= frame_time:
                result = pixels
                break
        return result

    return func


def keyframes_dict(frames_dict, name="animation"):
    """Create switchable animations from a dictionary of keyframe lists.

    Generates a function that returns GRB bytes based on time and the selected animation.
    This function is for use in a function matrix for an NPAnimation() object.

    Args:
        frames_dict (dict): Dictionary mapping animation names to keyframe lists.
            Each keyframe list should be in the format used by keyframes().
        name (str, optional): Keyword argument name for selecting animations. Defaults to "animation".

    Returns:
        function: Animation function func(time, **kwargs) that returns GRB bytes or list of GRB bytes.
    """
    for k in frames_dict:
        frames_dict[k].reverse()

    def func(time, **kwargs):
        result = [grb.OFF]
        if name in kwargs:
            anim_key = kwargs[name]
            if anim_key in frames_dict:
                frames = frames_dict[anim_key]
                period = frames[0][0]
                if period == 0:
                    period = 1
                for frame_time, pixels in frames:
                    if time % period >= frame_time:
                        result = pixels
                        break
        return result

    return func


class NPAnimation:
    """Main animation class for controlling NeoPixel LEDs with time-based functions.

    Animates LEDs using a function matrix that maps LED positions to animation functions.
    Each function in the matrix is called with the current time and optional keyword arguments,
    returning the color(s) to display.

    Example:
        Here's how to define a function matrix and call update_leds()::

            funcs = [
                [[0,1,2,3,4,5], hue_shift(period=5000)],  # Rainbow on LEDs 0-5
                [[13,14,16,17], switch(on=grb.WHITE, name="headlights")],  # Switchable headlights
                [[12,23], indicators(name="right_indicators")],  # Right turn signals
                [[15,20], indicators(name="left_indicators")],  # Left turn signals
                [[18,19,21,22], brake_lights()]  # Speed-responsive tail lights
            ]

            npa = NPAnimation(funcs, pin=24)
            while True:
                npa.update_leds(right_indicators=True, speed=5)

    Args:
        light_funcs (list): Function matrix - list of [led_positions, animation_function] pairs.
            led_positions is a list of LED indices, animation_function is a callable.
        pin (int, optional): GPIO pin number for NeoPixel data line. Defaults to 24.
        n_leds (int, optional): Total number of LEDs in the strip. If 0, auto-detects from
            the maximum LED position in light_funcs. Defaults to 0.

    Attributes:
        np (NeoPixel): The NeoPixel object controlling the LED strip.
        light_funcs (list): The function matrix passed during initialization.
        start_time (int): Internal timestamp for animation timing.
    """

    def __init__(self, light_funcs, pin: int = 21, n_leds: int = 0):
        if n_leds == 0:
            n_leds = max([max(n[0]) for n in light_funcs]) + 1
        self.np = NeoPixel(Pin(pin), n_leds)
        self.light_funcs = light_funcs
        self.start_time = utime.ticks_ms()

    def leds_off(self):
        """Turns all leds off."""
        self.np.fill(
            (
                0,
                0,
                0,
            )
        )
        self.np.write()

    def update_leds(self, time=None, **kwargs):
        """Update all LEDs based on current time and animation functions.

        Calls all animation functions in the function matrix and applies their
        output to the corresponding LED positions.

        Args:
            time (int, optional): Current time in milliseconds. If None, uses internal timer. Defaults to None.
            **kwargs: Keyword arguments passed to all animation functions (e.g., speed, headlights, etc.).
        """
        if not time:
            time = utime.ticks_diff(utime.ticks_ms(), self.start_time)
        for led_positions, func in self.light_funcs:
            grb = func(time, **kwargs)
            if type(grb) == bytes:
                for pos in led_positions:
                    self.np.buf[pos * 3 : pos * 3 + 3] = grb
            if type(grb) == list:
                i = 0
                for pos in led_positions:
                    self.np.buf[pos * 3 : pos * 3 + 3] = grb[i]
                    i += 1
                    if i >= len(grb):
                        i = 0
        self.np.write()
