#!python
"""A setuptools based setup module.

ToDo:
- Everything
"""

import setuptools

import simplifiedapp

import pathlib_vfs.google

setuptools.setup(**simplifiedapp.object_metadata(pathlib_vfs.google))
