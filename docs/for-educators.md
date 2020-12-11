# Using NI-edu as an educator
The publicly avaiable version of NI-edu is geared towards students. At the University of Amsterdam,
we also have an "teacher" version available: NI-edu-admin. The source material (i.e., the notebooks)
are identical, but they contain the solutions to the exercises (the "ToDos" and "ToThinks"). These
excercises are implemented such that they can be easily (and for a large part automatically) graded using
[nbgrader](https://nbgrader.readthedocs.io/en/stable/). Although not strictly necessary, we advise educators
to teach this course in a Jupyterhub environment. Using the shared environment provided by Jupyterhub results in a
smooth experience for both students and teachers. (Trust me, setting up personal Python environments of students' own
laptops is a nightmare.)

How to get access to NI-edu-admin? Email Lukas (L.Snoek@uva.nl), who will add you to the NI-edu-admin Github repository.
In case you have access to a Linux server to use for Jupyterhub, see the installation instructions below.

## Installing Jupyterhub
At the University of Amsterdam, we use Jupyterhub in combination with *nbgrader* on a shared server for our "labs" (i.e., the notebooks).
If you have access to a Linux server *and* you have root access, we highly recommend to use Jupyterhub (and *nbgrader*). 
By far the easiest way to install Jupyterhub (for relatively small classes) is through "[The Littlest Jupyterhub](https://tljh.jupyter.org/en/latest/index.html)" (TLJH). Read through the [installation](https://tljh.jupyter.org/en/latest/install/index.html) manual on the site. Again, this is only possible if you have root access (i.e., you have *sudo* rights).

## Installing *nbgrader*
Using the admin account, install *nbgrader* as follows:

```
sudo -E pip install nbgrader
```

Then, install the webinterface of the *nbgrader* package (including the Formgrader):

```
jupyter nbextension install --sys-prefix --py nbgrader --overwrite
jupyter nbextension enable --sys-prefix --py nbgrader
jupyter serverextension enable --sys-prefix --py nbgrader
```

Then, make sure there is a `nbgrader_config.py` file in the `~/.jupyter` folder. In this config file, the following variables should be set:

- `c.CourseDirectory.course_id` (e.g., "fMRI-introduction")
- `c.CourseDirectory.root` (e.g., "/home/{your_admin_account}/NI-edu-admin/fMRI-introduction")
- `c.ExecutePreprocessor.timeout` (I set it to `300`, because some exercises take a long time to run)

Note: your Formgrader tab may not yet "find" your `nbgrader_config.py` file, so it'll complain about it. Restarting the Hub usually works:

```
sudo tljh-config reload hub
```

Lastly, you need to add students to the database. Personally, I do that programatically using the command line interface of t

## Troubleshooting
**A student cannot login even though it's their first time logging in!**

The first time a student logs in, it sets their password. If this doesn't work, check whether you added the student to the "whitelist". Using an admin account, go to "Control panel", "Admin", and check if the student (e.g., "nim_01") is included in the list of Users. If not, click "Add user" and add the user (e.g., "nim_01", **not** "jupyter-nim_01").

**A student forgot their password and cannot log in!**

Check the [TLJH](https://tljh.jupyter.org/en/latest/howto/auth/firstuse.html) website under "Resetting user password".

**A student cannot access the Jupyterhub interface**

At the UvA, our Jupyterhub is behind a firewall that only accepts requests from the UvA network. Make sure students are connected to VPN!

**I can not generate an assignment!**

When you get an error when you generate an assignment, you most likely forgot a ### BEGIN SOLUTION or ### END SOLUTION marker or you added these to a non-test cell. 
