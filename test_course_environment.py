""" This script tests whether you're ready to start with the course! """
import os
import sys
import yaml
import os.path as op
from pathlib import Path

here = op.dirname(__file__)


print("Checking Python version ... \t\t\t", end='')
if sys.version[:5] == '3.8.5':
    has_py38 = True
    print("OK!")
else:
    has_py38 = False
    print("NOT OK!")

# Check anaconda
print("Checking anaconda installation ... \t\t", end='')
if 'conda' not in sys.executable:
    has_anaconda = False
    print("WARNING!")
else:
    has_anaconda = True
    print("OK!")

try:
    print("Checking niedu installation ... \t\t", end='')
    import niedu
except ImportError:
    has_niedu = False
    print("NOT OK!")
else:
    has_niedu = True
    print("OK!")

print('Checking FSL installation ... \t\t\t', end='')
if not 'FSLDIR' in os.environ:
    has_fsl = False
    print("NOT OK!")
else:
    has_fsl = True
    print("OK!")       


if not has_anaconda:
    print("\nWhile it's not strictly necessary, we highly recommend\n"
          "using the Anaconda distrution for Python! See this website\n"
          "for more information: https://lukas-snoek.com/NI-edu/getting_started/installation.html")
else:
    if not has_py38:
        print("\nYou seem to have the 'wrong' Python version. Please see the installation\n"
              "instructions here: https://lukas-snoek.com/NI-edu/getting_started/installation.html")

if not has_niedu:
    print("\nYou MUST install the 'niedu' package to follow this course.\n"
          "Please run the following to do so:\n"
          "'pip install .'")
