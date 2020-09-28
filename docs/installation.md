# Getting started
Bla bla

# Installation
Importantly, these courses assume you have Python version 3.7.3 installed. Most code will run properly with other Python versions (>3), but the compiled test functions will only work with Python 3.7.3 specifically.

To fetch the course material, clone this directory (or download as zip) and run:

```
pip install .
```

This will install the Python dependencies (`nibabel`, `matplotlib`, etc. etc.) for you, including the `niedu` package, containing utility functions and (compiled) test functions for the exercises.
For week 4-7 of the the *neuroimaging: introduction* course, you also need to install FSL (ideally version 6.0.1, but any version>=6 should work).

Once everything is installed, navigate to the course directory (e.g., fMRI-introduction/week_1) and run `jupyter notebook {name of notebook}.ipynb`.
