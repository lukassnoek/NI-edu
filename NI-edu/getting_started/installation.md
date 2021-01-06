# Installation
The course materials of fMRI-introduction and fMRI-pattern analyses contain Python-based Jupyter notebooks with tutorials and exercises (the "labs"). To do the labs, you need a working installation of Python (and [FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki)), the course materials themselves of course, and in addition some (f)MRI data that need to be downloaded separately. Below, we explain in detail how to do these three things.

## Software requirements: Python & FSL
Below, we discuss how to install Python and (optionally) how to install FSL.

### Installing Python
We *highly* recommend installing Python through Anaconda. To do so, go to the [Anaconda website](https://www.anaconda.com/products/individual) and download the latest *Anaconda installer* for your OS (Windows, MacOS, or Linux). Both the graphical and command-line installers are fine. After downloading the installer, run the installer. The default options suggested during installation are all fine (but no need to install the Pycharm IDE).

After installation, you need to create a new *environment* to make sure you're using the correct Python version. This is because the exercises (an important feature of the tutorials) only work when you have Python version 3.7.3 installed specifically. Fortunately, it's easy to create a new environment with Conda, the open-source package manager shipped with any Anaconda Python distribution. Creating a new environment is easiest through a command-line interface (CLI) in a *terminal*. Mac and Linux computers are shipped with a terminal, but we recommend that Windows users use the *Anaconda prompt* (which is shipped with Anaconda) as their terminal.

To create a new environment called `ni-edu` with the proper Python version after installing Anaconda, open a terminal and run the following command:

```
conda create -n niedu anaconda python=3.7.3
```

When promped to install a long list of packages (`Proceed ([y]/n)?`), type "y" and press enter. This will install a bunch of Python packages contained in the Anaconda distribution into the new environment. This may take a while. After the creation of the new environment (named "ni-edu") is done, you can activate the environment as follows:

```
conda activate ni-edu
```

Within this environment, you can start and run Jupyter notebooks that will run with the right Python version. Importantly, when running Jupyter notebooks from our courses, you *always* need to run them from this environment! 

To check whether everything worked as expected, run the following command in your terminal (in which the "ni-edu" environment should be active):

```
jupyter notebook
```

which will open a tab in your default browser with the Jupyter "home screen". Now, to create a new notebook, click on *New* &rarr; *Notebooks* &rarr; *Python 3*, which should open a new tab with a new notebook (by default titled "Untitled"). In the first cell (i.e., box with `In [ ]`), write the following code and press control + enter:

```python
import sys
sys.version
```

If you installed everything correctly, it should print out "3.7.3 (default ...)" etc. To open a tutorial notebook, navigate to the particular notebook you want to run in Jupyter file browser (e.g., *fMRI-introduction* &rarr; *week_1* &rarr; *python_for_mri.ipynb), and click on the file. This should open a new tab with the notebook. However, please go through the rest of the installation instructions below before starting to work on the tutorials.

### Running Python online (optional)
Some tutorials from this course can also be run in an online environment (instead of using a local Python installation). 

### FSL
In addition, a few tutorials will discuss how to work with the open-source MRI software package [FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki). FSL works natively on Linux and Mac and, if you're tech savvy, also on Windows (through the "Windows Subsystem for Linux"). Installation instructions for FSL can be found [here](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation). Note that FSL is only used in two labs (*First * run-level analyses* and *Group-level analyses*) in the fMRI-introduction course, and it discusses no new concepts, so it can safely be skipped.

## Downloading and installing the course materials
After installing Python, you need to download and install the actual course materials, which are stored on Github. Go to [https://github.com/lukassnoek/NI-edu](https://github.com/lukassnoek/NI-edu) and download the materials by either clicking on the green "Code" button and clicking "Download ZIP" and unzipping the zipped folder on your computer. Alternatively, you can run the following in your terminal (assuming you have git installed and know how it works):

```
git clone https://github.com/lukassnoek/NI-edu.git
```

Then, open a terminal, make sure your "ni-edu" environment is activated, and navigate to the new "NI-edu" folder (which you just downloaded). This folder contains all the course material (except for some extra data needed by the course). Additionally, it contains a custom Python package, `niedu`, that contains some code to check and grade the exercises from the tutorials. This package needs to be installed for the tutorials to work properly. To do so, within this folder (e.g., `/Users/lukas/NI-edu`), run the following command:

```
pip install .
```

Note the dot/period (.) right after `pip install` &mdash; this is intentional! Now, to check that everything worked properly, run the following command in your terminal:

```
python -c 'import niedu'
```

If it *doesn't* say `ModuleNotFoundError: No module named 'niedu'`, the package was correctly installed!

Some notebooks need some extra data that we couldn't store on Github because it's too large (>8GB). The next section describes how to download this data. Note that this extra data is only needed for two tutorials of the fMRI-introduction course (*First- & run-level analyses* and *Group-analyses*) and two tutorials of the fMRI-pattern-analysis course (*Decoding* and *RSA*). The other notebooks can be done without downloading the extra data.

## Downloading the NI-edu dataset
In the course materials, we included a script to download the data for the courses: `download_data.py`. For now, you can only download the data for the `fMRI-introduction` course. In the root directory of the course materials, run the following command:

```
python download_data.py {directory_to_save_data} --course introduction
```

where `{directory_to_save_data}` represents the location where you'd like to store the data. The dataset is about 8.2GB, so it might take a while to download everything. Then, after downloading the data, you need to install the `niedu` package again by running the command `pip install .` (note the dot).

## Running some post-installation stuff
Finally, we need to change some minor things in the dataset to make sure the notebooks run properly. Run the following in the root of course material directory:

```
python post_install.py
```

## Checking installation
To check whether everything is installed properly, run the `test_course_environment.py` script in the root of the course materials folder:

```
python test_course_environment.py
```

which should print out something like:

```
Checking Python version ...                     OK!
Checking anaconda installation ...              OK!
Checking nbgrader installation ...              OK!
Checking niedu installation ...                 OK!
Checking whether data is in place ...           OK!
Checking FSL installation ...                   OK!
Checking Jupyterhub data access ...             WARNING
```

You may ignore the `Checking Jupyterhub data access` warning (this is only for instructors).