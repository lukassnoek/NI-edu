""" This script tests whether you're ready to start with the course! """
import os
import sys
import os.path as op

here = op.dirname(__file__)


print("Checking Python version ... \t\t\t", end='')
py_version = sys.version.split(' ')[0]
if py_version == '3.9.16':
    has_py3916 = True
    print("OK!")
else:
    has_py3916 = False
    print("NOT OK!")

# Check anaconda
print("Checking anaconda installation ... \t\t", end='')
if 'conda' not in sys.executable:
    has_anaconda = False
    for p in sys.path:
        if '/tljh/' in p:
            # TLJH actually uses miniconda!
            has_anaconda = True
    if not has_anaconda:
        print("WARNING!")
    else:
        print("OK!")
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
          "using the Anaconda distrution for Python! See course website\n"
          "for more information: https://lukas-snoek.com/NI-edu/getting_started/installation.html")
else:
    if not has_py3916:
        print(f"\nYou seem to have the 'wrong' Python version (has {py_version}, need 3.9.16).\n"
              "Please see the installation instructions here:\n"
              "https://lukas-snoek.com/NI-edu/getting_started/installation.html")

if not has_niedu:
    print("\nYou MUST install the 'niedu' package to follow this course.\n"
          "Please run the following in the root directory:\n"
          "'pip install .'\n\n"
          "Note that you need to install this as root when working from\n"
          "a TLJH-based Jupyterhub setup!")
