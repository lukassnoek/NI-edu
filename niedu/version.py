from __future__ import absolute_import, division, print_function
from os.path import join as pjoin

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
_version_major = 0
_version_minor = 1
_version_micro = ''  # use '' for first of series, number for 1 and above
_version_extra = 'dev'
# _version_extra = ''  # Uncomment this for full releases

# Construct full version string from these.
_ver = [_version_major, _version_minor]
if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)

__version__ = '.'.join(map(str, _ver))

CLASSIFIERS = ["Development Status :: 3 - Alpha",
               "Environment :: Console",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering"]

# Description should be a one-liner:
description = "NI-edu: public NeuroImaging courses from the University of Amsterdam"
# Long description will go up on the pypi page
long_description = """
NI-edu
========
NI-edu is a repository with (as of now) two NeuroImaging courses from the University
of Amsterdam. It is freely accessible and (given a proper Python environment) can be
run on any system. It uses a publicly available MRI dataset acquired at our 3T scanner
at the University of Amsterdam.

To get started with one or both of these courses, go to the repository README_.
.. _README: https://github.com/lukassnoek/NI-edu/blob/master/README.md

License
=======
``NI-edu`` is licensed under the terms of the MIT license. See the file
"LICENSE" for information on the history of this software, terms & conditions
for usage, and a DISCLAIMER OF ALL WARRANTIES.
All trademarks referenced herein are property of their respective holders.
Copyright (c) 2019--, Lukas Snoek, University of Amsterdam.
"""

NAME = "niedu"
MAINTAINER = "Lukas Snoek"
MAINTAINER_EMAIL = "lukassnoek@gmail.com"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "http://github.com/lukassnoek/NI-edu"
DOWNLOAD_URL = ""
LICENSE = "MIT"
AUTHOR = "Lukas Snoek"
AUTHOR_EMAIL = "lukassnoek@gmail.com"
PLATFORMS = "OS Independent"
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__

REQUIRES = [
    "numpy",
    "scipy",
    "matplotlib",
    "pandas",
    "scikit-learn",
    "seaborn",
    "nibabel",
    "nilearn",
    "click",
    "jupyter",
    "pyyaml",
    "awscli",
    "tqdm",
    "imageio"
]
