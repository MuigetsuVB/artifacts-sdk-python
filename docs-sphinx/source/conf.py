# Configuration file for the Sphinx documentation builder.
# Artifacts MMO Python SDK -- Documentation joueurs

import os
import sys

# -- Path setup ---------------------------------------------------------------
sys.path.insert(0, os.path.abspath("../../src"))

# -- Project information ------------------------------------------------------
project = "Artifacts MMO SDK"
copyright = "2026, Artifacts MMO SDK Contributors"
author = "Artifacts MMO SDK Contributors"
release = "0.2.1"
version = "0.2"

# -- General configuration ----------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
]

templates_path = ["_templates"]
exclude_patterns = []
language = "en"

# Napoleon settings (Google/NumPy docstrings)
napoleon_google_docstrings = True
napoleon_numpy_docstrings = True
napoleon_include_init_with_doc = True

# Autodoc settings
autodoc_member_order = "bysource"
autodoc_typehints = "description"

# -- Options for HTML output ---------------------------------------------------
html_theme = "furo"
html_title = "Artifacts MMO SDK"
html_static_path = ["_static"]

html_theme_options = {
    "navigation_with_keys": True,
}

# -- Intersphinx mapping -------------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
