""" This script tests whether you're ready to start with the course! """
import os
import sys
import yaml
import os.path as op

here = op.dirname(__file__)


print("Checking Python version ... \t\t\t", end='')
if sys.version[:5] == '3.7.3':
    has_py37 = True
    print("OK!")
else:
    has_py37 = False
    print("NOT OK!")

# Check anaconda
print("Checking anaconda installation ... \t\t", end='')
if 'conda' not in sys.executable:
    has_anaconda = False
    print("WARNING!")
else:
    has_anaconda = True
    print("OK!")

# Check nbgrader
try:
    print('Checking nbgrader installation ... \t\t', end='')
    import nbgrader
except ImportError:
    has_nbgrader = False
    print("NOT OK!")
else:
    if nbgrader.__version__ != '0.6.1':
        has_nbgrader = False
        print("NOT OK!")
    else:
        has_nbgrader = True
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

print("Checking whether data is in place ... \t\t", end='')
with open('course_settings.yml', 'r') as f_in:
    settings = yaml.safe_load(f_in)

data_dir = settings['data_dir']
if not op.isdir(data_dir):
    has_data = False
    print("NOT OK!")
else:
    has_data = True
    print("OK!")

print('Checking FSL installation ... \t\t\t', end='')
if not 'FSLDIR' in os.environ:
    has_fsl = False
    print("NOT OK!")
else:
    has_fsl = True
    print("OK!")       

print('')

if not has_py37:
    print("You either do not have Python installed or have the 'wrong' version.\n"
          "We recommend installing the Anaconda Python distribution from this URL:\n"
          "https://repo.anaconda.com/archive/. Please download the version from July 2019 \n"
          "(starting with Anaconda3-2019.07).\n"
          "If you have Python installed, but not version 3.7.3, we recommend either installing\n"
          "the July 2019 version (which contains Python 3.7.3.) or create a new Python environment\n"
          "with Python 3.7.6. (e.g., using conda: conda create -n ni-edu python=3.7.3).\n"
          "The specific version has to do with the fact that the answer-modules are compiled with this\n"
          "specific version, and won't work otherwise!\n")

if not has_anaconda:
    print("While it's not strictly necessary, we highly recommend\n"
          "using the Anaconda distrution for Python!")

if not has_nbgrader:
    print("The 'nbgrader' package was not installed (or not the right version; should be 0.6.1).\n"
          "While the nbgrader package is not strictly necessary,\n"
          "you need to install it if you want do do/check the exercises!\n"
          "Install nbgrader using 'pip install -U nbgrader'.")

if not has_niedu:
    print("You MUST install the 'niedu' package to follow this course.\n"
          "Please run 'pip install .' to do so!")

if not has_data:
    print("You MUST download the data for this course, otherwise\n"
          "you cannot run most of the notebooks. Please run\n"
          "'bash download_data.sh' to do so (uses 'curl').")

if not has_fsl:
    print("While not strictly necessary, you need FSL (version 6.0.1) for some of the exercises.\n"
          "Download the software from https://fsl.fmrib.ox.ac.uk/fsl/fslwiki (MAC/LINUX only).")
