# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Second_Chance'
copyright = '2024, Michael Pagano, Victor Tran, Ben Stephenson, Enes Mance, Chung Ying Lee'
author = 'Michael Pagano, Victor Tran, Ben Stephenson, Enes Mance, Chung Ying Lee'
release = '5.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os 
import sys 

# Add directories to PATH
sys.path.insert(0, os.path.abspath('..')) # Project root directory
sys.path.insert(0, os.path.abspath('../src')) # src directory


extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
