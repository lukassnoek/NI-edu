# Getting started
The course materials of fMRI-introduction and fMRI-pattern analyses contain lecture slides and Jupyter notebooks with tutorials and exercises (the "labs"). The lecture slides can be found on this website, but you need to download the lab materials yourself to do the labs. Additionally, some labs need data that need to be downloaded separately. Below, we explain how to get your computer ready for the course. 

The labs of both courses are taught using [Jupyter notebooks](https://jupyter.org/), which are browser-based computational nodebooks that are able to run code (e.g., Python, R, and Julia) as well as display text and visualizations. For each lab, there is a (or multiple) notebook(s) with text, Python code, and exercises meant to explain important concepts in fMRI analysis. In addition, we will work with an open-source MRI software package called [FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki). Unfortunately, FSL can only be installed on Linux or Mac, but it is only used in two labs (week 5 and week 6) in fMRI-introduction, so FSL is not *strictly* necessary.

So, in terms of software, you need to have a working installation of Python (ideally version 3.7.3), including the Jupyter notebook package, and FSL (although the latter is not necessary for 95% of the lab material).

Below, we describe the three things you need to do to work through the labs.

## Installing Python
We *highly* recommend installing Python through Anaconda. To do so, go to the [Anaconda website](https://www.anaconda.com/products/individual) and install the latest version. After installation, you need to create a new *environment* to make sure you're using the correct Python version. This is because the exercises (an important feature of the labs) only work when you have Python version 3.7.3 installed specifically. Fortunately, it's easy to create a new environment with Conda, the open-source package manager shipped with any Anaconda Python distribution. To create a new environment called `ni-edu` with the proper Python version after installing Anaconda, open a terminal and run the following command:

```
conda create -n niedu anaconda python=3.7.3
```

When promped to install a long list of packages (Proceed ([y]/n)?), type "y" and press enter. This will install a bunch of Python packages contained in the Anaconda distribution into the new environment. This may take a while. After the creation of the new environment (named "ni-edu") is done, you can activate the environment as follows:

```
conda activate ni-edu
```

Now you can start and run Jupyter notebooks that will run with the right Python version. Importantly, when running Jupyter notebooks from our courses, you *always* need to run them from this environment! 

To check whether everything worked as expected, run the following command in your terminal (in which the "ni-edu" environment should be active):

```
jupyter notebook
```

which will open a tab in your default browser with the Jupyter "home screen". Now, to create a new notebook, click on "New", "Notebooks", "Python 3", which should open a new tab with a new notebook (by default titled "Untitled"). In the first cell (i.e., box with `In [ ]`), write the following code and press control + enter:

```python
import sys
sys.version
```

If you installed everything correctly, it should print out "3.7.3 (default ...)" etc. 

## Downloading and installing the course materials
After installing Python, you need to download and install the actual course materials, which are stored on Github. Go to [https://github.com/Neuroimaging-UvA/NI-edu](https://github.com/Neuroimaging-UvA/NI-edu) and download the materials by either clicking on the green "Code" button and clicking "Download ZIP" and unzipping the zipped folder on your computer *or* running the following in your terminal (assuming you have git installed and know how it works):

```
git clone https://github.com/Neuroimaging-UvA/NI-edu.git
```

Then, open a terminal, make sure your "ni-edu" environment is activated, and navigate to the new "NI-edu" folder (which you just downloaded). This folder contains all the course material (except for some extra data needed by the course). Within this folder, run the following command:

```
pip install .
```

which will install the custom Python package, `niedu`, which we'll use in the course (e.g., for checking exercises). Now, to check that everything worked properly, run the following command in your terminal:

```
python -c 'import niedu'
```

If it *doesn't* say "ModuleNotFoundError: No module named 'niedu'", the package was correctly installed! At this point, you can start working on the labs. To do so, in a terminal (again, with the "ni-edu" environment activated), navigate to the lab you want to do (e.g., `fMRI-introduction/week_1`) and run `jupyter notebook {name_of_notebook.ipynb}`. For example:

```
jupyter notebook python_tutorial.ipynb
```

Some notebooks need some extra data that we couldn't store on Github because it's too large (>8GB). The next section describes how to download this data. Note that this extra data is only needed for week 5, 6, and 7 of fMRI-introduction and week 2 and 3 of fMRI-pattern-analysis. The other notebooks can be done without downloading the extra data.

## Downloading the NI-edu dataset
In the course materials, we included a script to download the data for the courses: `download_data.p`. For now, you can only download the data for the `fMRI-introduction` course. In the root directory of the course materials, run the following command:

```
python download_data.py {directory_to_save_data} --course introduction
```

where `{directory_to_save_data}` represents the location where you'd like to store the data. The dataset is about 8GB, so it might take a while to download everything. Then, after downloading the data, you need to install the `niedu` package again by running the command `pip install .` again.

## Running some post-installation stuff
Finally, we need to change some minor things in the dataset to make sure the notebooks run properly. Run the following in the root of course material directory:

```
python post_install.py
```