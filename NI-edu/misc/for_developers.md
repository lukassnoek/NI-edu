# For developers
If you wish to contribute to the course materials, you can find some instructions below.

## Building the book
To build the book, make sure you have the [jupyter book](https://jupyterbook.org) package installed. Then, run the following in the root of the repository:

```
./build_book
```

Note that this does not work on Windows (Mac/Linux) only.

## Using `nbgrader`
We use [nbgrader](https://nbgrader.readthedocs.io/en/stable/) to convert the *solution* notebooks (which contain the solutions to the exercises) to the *tutorial* notebooks (without the solutions). If you do this yourself, make sure you use the `nbgrader_config.py` file from this repository (because we use the directory names "solutions" and "tutorials" instead of "source" and "release"). 

To regenerate the notebooks from week 1 (week 2 doesn't have any notebooks), run in the root of this repository the following command:

```
nbgrader generate_assignment --force week_*
```

## Testing
To test the notebooks, run the following (note: needs the packages `pytest` and `nbval`; Mac/Linux only):

```
./test_material
```