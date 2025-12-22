# Configuration file for the Sphinx documentation builder.

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Mock MicroPython modules that don't exist in regular Python
sys.modules["neopixel"] = MagicMock()
sys.modules["machine"] = MagicMock()
sys.modules["utime"] = MagicMock()

# -- Project information -----------------------------------------------------
project = "np_animation"
copyright = "2025, Anton Vanhoucke"
author = "Anton Vanhoucke"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- Options for autodoc -----------------------------------------------------
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

# -- Options for intersphinx -------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
