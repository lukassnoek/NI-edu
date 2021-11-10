# For educators
The publicly avaiable version of NI-edu is geared towards students. At the University of Amsterdam,
we also have an "teacher" version available: NI-edu-admin. The source material (i.e., the notebooks)
are identical, but they contain the solutions to the exercises (the "ToDos" and "ToThinks"). These
excercises are implemented such that they can be easily (and for a large part automatically) graded using
[nbgrader](https://nbgrader.readthedocs.io/en/stable/). Although not strictly necessary, we advise educators
to teach this course in a Jupyterhub environment. Using the shared environment provided by Jupyterhub results in a
smooth experience for both students and teachers. (Trust me, setting up personal Python environments of students' own
laptops is a nightmare.)

How to get access to NI-edu-admin? Email Lukas (his email address can be found on his [website](https://lukas-snoek.com/)), who will add you to the NI-edu-admin Github repository. In case you have access to a Linux server to use for Jupyterhub, see the installation instructions below.

## Installing Jupyterhub
At the University of Amsterdam, we use Jupyterhub in combination with *nbgrader* on a shared server for our "labs" (i.e., the notebooks).
If you have access to a Linux server *and* you have root access, we highly recommend to use Jupyterhub (and *nbgrader*). By far the easiest way to install Jupyterhub (for relatively small classes) is through "[The Littlest Jupyterhub](https://tljh.jupyter.org/en/latest/index.html)" (TLJH). Read through the [installation](https://tljh.jupyter.org/en/latest/install/index.html) manual on the site. Again, this is only possible if you have root access (i.e., you have *sudo* rights).

After installing TLJH, there are a few things I'd recommend you do. The first, and most important thing, is to enable HTTPS. To do so, check the [TLJH guide](https://tljh.jupyter.org/en/latest/howto/admin/https.html#howto-admin-https). 

As an example, for the UvA Linux server, you'd do this by running the following commands:

```
sudo tljh-config set https.enabled true
sudo tljh-config set https.letsencrypt.email {Lukas' email}
sudo tljh-config add-item https.letsencrypt.domains neuroimaging.lukas-snoek.com
sudo tljh-config reload proxy
```

Second, I'd recommend increasing the idle timeout (i.e., maximum time in seconds that a server can be inactive before it will be shutdown). By default, each notebook server is shut down after 10 minutes of inactivity, which is a bit short. To increase this, run the following (to increase it to 24hrs):

```
sudo tljh-config set services.cull.timeout 86400
sudo tljh-config reload
```

## Installing *nbgrader*

:::{warning}
Currently, the latest version of `nbgrader` (0.6.2) has a bug that breaks the formgrader interface, which is fixed in the master branch on Github. So, _don't_ install `nbgrader` from PyPI (using `pip install nbgrader`), but install `nbgrader` from source as follow:

```
sudo -E pip install git+https://github.com/jupyter/nbgrader.git@master
```

:::

Then, install the webinterface of the *nbgrader* package (including the Formgrader):

```
sudo jupyter nbextension install --sys-prefix --py nbgrader --overwrite
sudo jupyter nbextension enable --sys-prefix --py nbgrader
sudo jupyter serverextension enable --sys-prefix --py nbgrader
```

Then, make sure there is a `nbgrader_config.py` file in the `~/.jupyter` folder. In this config file, the following variables should be set:

- `c.CourseDirectory.course_id` (e.g., "fMRI-introduction")
- `c.CourseDirectory.root` (e.g., "/home/{your_admin_account}/NI-edu-admin/fMRI-introduction")
- `c.ExecutePreprocessor.timeout` (I set it to `300`, because some exercises take a long time to run)

Note: your Formgrader tab may not yet "find" your `nbgrader_config.py` file, so it'll complain about it. Restarting the Hub usually works:

```
sudo tljh-config reload hub
```

Lastly, you need to add students to the database. Personally, I do that programatically using the command line interface of the *nbgrader* package but you can also do this manually in the Formgrader. Note: **you don't have to create the Linux accounts yourself!** This is handles by the Jupyterhub interface.

:::{warning}
Important: when adding users to the database, make sure you enter their Linux account name in the "Student ID" field (e.g., `jupyter-nim_01`), _not_ their Jupyterhub ID (e.g., `nim_01`). This is important because `nbgrader` only "knows" about the Linux accounts, not the Jupyterhub users. 
:::


## Install `niedu`
Finally, you need to install the `niedu` package for utilities and tests for the tutorials. Importantly, the compiled test functions only work with Python version 3.8.5, which is not the default version installed by TLJH. To update the version to 3.8.5, run the following command from the user account you used to install TLJH:

```
export PATH=/opt/tljh/user/bin:${PATH}
source /opt/tljh/user/bin/activate
sudo PATH=${PATH} conda install python=3.8.5
```

Now, you can install the `niedu` package as follows (note the period at the end, which is part of the command):

```
sudo -E pip install .
```

To check your installation at this point, you can run the following command in the root of the repository:

```
python test_course_enviroment.py
```

## Enable SSH
For some of the tutorials, students need to access the server through SSH (via X2Go). When Jupyterhub creates the student accounts, SSH is *not* enabled by default.  To do so, do the following *for every student account*:

```
# Add user to group `users`
sudo usermod -a -G users ${username}

# Change default shell to `bash`
sudo chsh -s /bin/bash $username

# Change password
sudo passwd $username
```

The last command will trigger user input, which you can use to enter a password. Yes, you need to do this manually. Yes, there are ways to automate this, but this comes with security risks, so I'd advise against this. I'd recommend using the same, secure (long, combination of letters, digits, and symbols) password for all users.

For a script version that does this for all users in a loop, check the `enable_ssh.sh` file in the `sysadmin` directory in the `NI-edu-admin` repository.

## Troubleshooting
See the short troubleshooting guide when encountering issues.

### The formgrader is not loading

Did you install `nbgrader` from PyPI (using `pip install nbgrader`) and is it version 0.6.2? Then reinstall nbgrader from source (`sudo -E pip install git+https://github.com/jupyter/nbgrader.git@master`), reinstall the nbextension and serverextension, and reload the hub (`sudo tljh-config reload hub`).

### Letsencrypt cannot renew the certificates

Letsencrypt renews certificates using a test that uses port 443. At the UvA, we only allow connections with port 443 from the UvA network (so you need to be connected to VPN), so the renewal will fail. To renew the certificates, temporarily open up port 443 (`sudo ufw allow 443`), run the renew command (`certbot renew`), and close the port again (run `sudo ufw status numbered`, check the number of the rule for port 443, and then run `sudo ufw delete {nr of rule}`). 

### A student cannot login even though it's their first time logging in!

The first time a student logs in, it sets their password. If this doesn't work, check whether you added the student to the "whitelist". Using an admin account, go to "Control panel", "Admin", and check if the student (e.g., "nim_01") is included in the list of Users. If not, click "Add user" and add the user (e.g., "nim_01", **not** "jupyter-nim_01").

### A student forgot their password and cannot log in!

Check the [TLJH](https://tljh.jupyter.org/en/latest/howto/auth/firstuse.html) website under "Resetting user password".

### A student cannot access the Jupyterhub interface

At the UvA, our Jupyterhub is behind a firewall that only accepts requests from the UvA network. Make sure students are connected to VPN!

### I can not generate an assignment!

When you get an error when you generate an assignment, you most likely forgot a ### BEGIN SOLUTION or ### END SOLUTION marker or you added these to a non-test cell. 

### Students cannot see an assignment!

Make sure that you, in the formgrader, generated *and* released the assignment!
