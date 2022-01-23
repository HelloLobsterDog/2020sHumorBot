# This very minimal setup.py relies on the metadata in setup.cfg
# Per modern setuptools documentation, this use case is deprecated, and you're supposed to rely exclusively on setup.cfg via build and pip,
# however, given how in flux python's packaging mechanisms are, to avoid confusion, this file is provided so those used to using setup.py can still do so
# without having to learn something that the language may just make deprecated in favor of something else.
from setuptools import setup
setup()