# NI-edu
Main repository for student-version of the neuroimaging (MRI) courses. To get access to the admin-version (including answers to the exercises/assignments), email Lukas (address on top of the organization's [page](https://github.com/Neuroimaging-UvA)).

**WARNING**: this is work-in-progress!

Check out the (very incomplete) [documentation](https://neuroimaging-uva.github.io/NI-edu/)!

## Contents
This repository contains two courses: *neuroimaging: introduction* and *neuroimaging: pattern analysis*, containing course material from the two courses with the same name taught at the University of Amsterdam (at the Research Master Psychology). The introductory course is an eight-week course, containing seven computer labs in which students have to work through one or multiple jupyter notebooks with exercises. These notebooks (but not the lecture slides and material from the seminars) are available in this repository. We highly recommend doing the *introduction* course **before** doing the *pattern analysis* course. The contents of the two courses are listed below.

### Neuroimaging: introduction
* Week 1: Python tutorial (including working with Nifti images)
* Week 2: GLM (part 1: estimation)
* Week 3: GLM (part 2: inference) and design of experiments
* Week 4: Preprocessing
* Week 5: Linux and the command line, FSL, and introduction to multilevel analyses 
* Week 6: Grouplevel models, multiple comparison correction, and ROI analyses
* Week 7: Introduction to [nilearn](https://nilearn.github.io/) and [nistats](https://nistats.github.io)

### Neuroimaging: pattern analysis
*THIS COURSE IS BEING UPDATED. WILL BE ONLINE ~MAY 2020*

* Week 1: pattern estimation (+nilearn/nistats)
* Week 2: machine learning ("decoding")
* Week 3: representational similarity analysis
* Week 4: final project (using publicly available data)

## Installation
Importantly, these courses assume you have Python version 3.7.3 installed. Most code will run properly with other Python versions (>3), but the compiled test functions will only work with Python 3.7.3 specifically.

To fetch the course material, clone this directory (or download as zip) and run:

```
pip install .
```

This will install the Python dependencies (`nibabel`, `matplotlib`, etc. etc.) for you, including the `niedu` package, containing utility functions and (compiled) test functions for the exercises.

For week 4-7 of the the *neuroimaging: introduction* course, you also need to install FSL (ideally version 6.0.1, but any version>=6 should work).

Once everything is installed, navigate to the course directory (e.g., neuroimaging-introduction/week_1) and run `jupyter notebook {name of notebook}.ipynb`.

