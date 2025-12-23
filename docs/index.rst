NeoPixel Animation Library Documentation
=========================================

Introduction
------------

``np_animation`` is a MicroPython library for driving NeoPixel animations with time functions and keyframes. It provides a convenient way to create complex LED animations using a function-based approach.

Installation
------------

Recommended: Using ViperIDE Package Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to install ``np_animation`` on your MicroPython device:

1. Open `viperIDE.org <https://viperIDE.org>`_
2. Navigate to **Tools > Package Manager**
3. Select **Install package via link**
4. Enter: ``github:antonvh/np_animation``

LMS-ESP32
~~~~~~~~~

The package should be frozen in the latest firmeware build on https://firmware.antonsmindstorms.com.
If not, use the ViperIDE Package Manager method above.

Alternative Methods
~~~~~~~~~~~~~~~~~~~

Copy the ``np_animation.py`` file to your MicroPython device.

Quick Start
-----------

Here's a simple example to get you started:

.. literalinclude:: ../examples/basic_rainbow.py
   :language: python
   :linenos:

API Reference
=============

This section contains the full API documentation generated from the docstrings in the code.

Color Conversion Functions
---------------------------

.. autofunction:: np_animation.np_animation.hsl_to_rgb
.. autofunction:: np_animation.np_animation.rgb_to_hsl
.. autofunction:: np_animation.np_animation.to_grb
.. autofunction:: np_animation.np_animation.from_grb

Color Enumerator Classes
-------------------------

.. autoclass:: np_animation.np_animation.grb
   :members:
   :undoc-members:

.. autoclass:: np_animation.np_animation.rgb
   :members:
   :undoc-members:

Animation Functions
-------------------

.. autofunction:: np_animation.np_animation.indicators
.. autofunction:: np_animation.np_animation.brake_lights
.. autofunction:: np_animation.np_animation.switch
.. autofunction:: np_animation.np_animation.delayed_switch
.. autofunction:: np_animation.np_animation.hue_shift
.. autofunction:: np_animation.np_animation.pulse
.. autofunction:: np_animation.np_animation.knight_rider
.. autofunction:: np_animation.np_animation.knight_rider_gen
.. autofunction:: np_animation.np_animation.keyframes
.. autofunction:: np_animation.np_animation.keyframes_dict

Main Animation Class
--------------------

.. autoclass:: np_animation.np_animation.NPAnimation
   :members:
   :undoc-members:
   :show-inheritance:

Examples
========

This section contains examples of using the np_animation library.

Basic Rainbow Animation
-----------------------

The simplest example showing a rainbow color cycle:

.. literalinclude:: ../examples/basic_rainbow.py
   :language: python
   :linenos:

Vehicle Lighting System
-----------------------

A complete vehicle lighting system with headlights, turn signals, and brake lights:

.. literalinclude:: ../examples/vehicle_lighting.py
   :language: python
   :linenos:

Knight Rider Effect
-------------------

Classic Knight Rider scanner effect:

.. literalinclude:: ../examples/knight_rider.py
   :language: python
   :linenos:

Emergency Lights
----------------

Emergency vehicle light pattern using keyframes:

.. literalinclude:: ../examples/emergency_lights.py
   :language: python
   :linenos:

Multi-Layer Animation
---------------------

Complex animation with multiple layers:

.. literalinclude:: ../examples/multi_layer.py
   :language: python
   :linenos:

Color Utilities
---------------

Using color conversion utilities:

.. literalinclude:: ../examples/color_utils.py
   :language: python
   :linenos:

Testing
-------

The library includes comprehensive tests. Run them with::

    pytest tests/test_np_animation.py -v

Tests cover:

* RGB to GRB and GRB to RGB conversions
* RGB to HSL and HSL to RGB conversions
* Round-trip conversion accuracy
* Color enumerator values
* Correspondence between rgb and grb enumerators

License
-------

MIT License

See LICENSE file for details.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

