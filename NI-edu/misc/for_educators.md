# For educators
The publicly available version of NI-edu is geared towards students At the University of Amsterdam, but
we also have an "teacher" version available: NI-edu-admin. The source material (i.e., the notebooks)
are identical, but they contain the solutions to the exercises (the "ToDos" and "ToThinks"). These
excercises are implemented such that they can be easily (and for a large part automatically) graded using
[nbgrader](https://nbgrader.readthedocs.io/en/stable/). Although not strictly necessary, we advise educators
to teach this course in a Jupyterhub environment. Using the shared environment provided by Jupyterhub results in a
smooth experience for both students and teachers. (Trust me, setting up personal Python environments of students' own
laptops is a nightmare.)

How to get access to NI-edu-admin? Email Lukas (his email address can be found on his [website](https://lukas-snoek.com/)), who will add you to the NI-edu-admin Github repository. In case you have access to a Linux server to use for Jupyterhub, see the installation instructions below.

## Installing Jupyterhub
At the University of Amsterdam, we use Jupyterhub on a Linux (Ubuntu 20.04 with MATE desktop) in combination with *nbgrader* on a shared server for our "labs" (i.e., the notebooks). If you have access to a Linux server (which can be virtual, like an AWS/Azure/Google cloud instance) *and* you have root access, we highly recommend to teach this course using Jupyterhub (and *nbgrader*). By far the easiest way to install Jupyterhub (for relatively small classes) is through "[The Littlest Jupyterhub](https://tljh.jupyter.org/en/latest/index.html)" (TLJH). Setting up TLJH in combination with *nbgrader* and the NI-edu materials can be a bit tricky, so I'm documenting the installation procedure below.

### 1. Install TLJH
Read through the [TLJH installation manual](https://tljh.jupyter.org/en/latest/install/index.html). Again, this is only possible if you have root access (i.e., you have *sudo* rights). Follow step 1 ("Installing The Littlest Jupyterhub") until (sub)step 5. Step 5-7 can, at least in the case of the UvA TUX server, not be executed literally, because all access to the ports of the server are restricted to the IP range of the UvA. So instead of accessing Jupyterhub through your browser to complete step 5-7, create a remote desktop connection with X2Go.

Using the remote desktop, you can complete (sub)step 5-7 and step 2 of the manual ("Adding more users"). For example, you can add a co-teacher as "admin" to the course. For example, to add Lukas Snoek (Linux username: lukassnoek) as a co-teacher, go to the "Admin" tab in the Jupyterhub interface, click on "Add Users", and fill in his username (i.e., "lukassnoek", *not* "jupyter-lukassnoek") and check the "Admin" box.

It is important to remember that no one will be able to access the Jupyterhub interface unless his/her username has been added ("whitelisted") using this interface (Admin tab; Add Users) &mdash; even if this person already has a Linux (or even Jupyterhub) account on the server!

You can skip step 3 ("Install conda / pip packages for all users") for now. We'll get to this later.

### 2. Enable SSL encryption
The next step is to enable SSL encryption (step 4 of the installation manual). Please see the instructions [here](https://tljh.jupyter.org/en/latest/howto/admin/https.html#howto-admin-https). I'm going to assume that Letsencrypt will be used for SSL certificates (which is what we've always done). For the TUX server, you'd run the following commands

```
sudo tljh-config set https.enabled true
sudo tljh-config set https.letsencrypt.email {your email}
sudo tljh-config add-item https.letsencrypt.domains neuroimaging.lukas-snoek.com
```

Now, before you reload the proxy (`sudo tljh-config reload proxy`), you need to make sure that port 80 is actually accessible (which isn't the case for the TUX) because Letsencrypt will perform a "verification" necessary to enable SSL encryption. To do so, run `sudo ufw allow 80`. Then, run `sudo tljh-config reload proxy` and finally close port 80 again by running `sudo ufw delete allow 80`. 

### 3. Configure TLJH
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

Letsencrypt renews certificates using a test that uses port 80. At the UvA, we don't allow connections to this port, so the renewal will fail. To renew the certificates, temporarily open up port 80 (`sudo ufw allow 80`), run the renew command (`certbot renew`), and close the port again (run `sudo ufw status numbered`, check the number of the rule for port 80, and then run `sudo ufw delete {nr of rule}`). 

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
