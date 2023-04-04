# For educators
The publicly available version of NI-edu is geared towards students At the University of Amsterdam, but
we also have an "teacher" (or "admin") version available: NI-edu-admin. The source material (i.e., the notebooks)
are identical, but they contain the solutions to the exercises (the "ToDos" and "ToThinks"). These
excercises are implemented such that they can be easily (and for a large part automatically) graded using
[nbgrader](https://nbgrader.readthedocs.io/en/stable/). 

How to get access to NI-edu-admin? Email Lukas (his email address can be found on his [website](https://lukas-snoek.com/)), who will add you to the NI-edu-admin Github repository. We'd like to ask those added to the admin repository not to share the materials with others (e.g. in a separate Github repository).

Although not strictly necessary, we advise educators to teach this course in a Jupyterhub environment in combination with [nbgrader](https://nbgrader.readthedocs.io/en/stable/). This setup allows for easy distribution, submission, and grading of the course's notebooks with exercises. Setting up Jupyterhub, nbgrader, and the course materials is far from trivial, though. Below, we outline how this is done.

## Installing Jupyterhub + `nbgrader`

Jupyterhub can be installed on your own server or a virtual server (e.g., from AWS/Azure/Google Cloud). The only prerequisity is that the server runs Ubuntu (18.04 or 20.04) and you have root access. By far the easiest way to install Jupyterhub (for relatively small classes) is through "[The Littlest Jupyterhub](https://tljh.jupyter.org/en/latest/index.html)" (TLJH). 

### 1. Install TLJH
Read through the [TLJH installation manual](https://tljh.jupyter.org/en/latest/install/index.html). Again, this is only possible if you have root access (i.e., you have *sudo* rights). Follow step 1 ("Installing The Littlest Jupyterhub") until (sub)step 5. Step 5-7 can, at least in the case of the UvA TUX server, not be executed literally, because all access to the ports of the server are restricted to the IP range of the UvA. So instead of accessing Jupyterhub through your browser to complete step 5-7, create a remote desktop connection (e.g., with [X2Go](https://wiki.x2go.org/doku.php/download:start) and complete these steps in the remote desktop environment.

You can skip step 3 ("Install conda / pip packages for all users") for now. We'll get to this later.

### 2. Enable SSL encryption
The next step is to enable SSL encryption (step 4 of the installation manual). Please see the instructions [here](https://tljh.jupyter.org/en/latest/howto/admin/https.html#howto-admin-https). I'm going to assume that Letsencrypt will be used for SSL certificates (which is what we've always done). For the TUX server, you'd run the following commands

```
sudo tljh-config set https.enabled true
sudo tljh-config set https.letsencrypt.email {your email}
sudo tljh-config add-item https.letsencrypt.domains {your_domain_name}
```

Now, before you reload the proxy (`sudo tljh-config reload proxy`), you need to make sure that port 80 is actually accessible (which isn't the case for the server at the UvA) because Letsencrypt will perform a "verification" necessary to enable SSL encryption. To do so, run `sudo ufw allow 80`. Then, run `sudo tljh-config reload proxy` and finally close port 80 again by running `sudo ufw delete allow 80`. 

Finally, Jupyterhub communicates through port 443, so this needs to be open to the world! At the UvA, we restrict access to our servers (through any port) to the IP range of the UvA network, which means that you can only access the server if you're either at the UvA and connected to the UvA network or connected to the UvA VPN. Assuming you have a firewall enabled (through `ufw`), you can open up port 443 with restricted access to a particular IP address by running:

```
sudo ufw allow proto tcp from {your_ip_address} to any port 443
```

After opening up port 443 (if it wasn't already), you should be able to access Jupyterhub through your own browser (e.g., at *https://your.domain.com*). Make sure you actually access the HTTP**S** version (i.e., the SSL-encrypted website), and not the HTTP website. If not, reload the TLJH environment with `sudo tljh-config reload`.

### 3. Configure TLJH
Next, I recommend to change some of the default TLJH parameters. First, increase the idle timeout (i.e., maximum time in seconds that a user's notebook server can be inactive before it will be shut down). By default, each notebook server is shut down after 10 minutes of inactivity, which is a bit short. To increase this, run the following (to increase it to 24 hrs):

```
sudo tljh-config set services.cull.timeout 86400
sudo tljh-config reload
```

### 4. Configure Python
Currently (April 2023), the default TLJH python version (3.9.16) is the same as the version used by 
the course. If not (e.g., either TLJH or the course updates its python version), it is important to make sure to change the TLJH version such that it matches the course's version, because the compiled test functions only work with the Python version used in the course. To change to Python version X (where X may be `3.10.2` or something), run the following command from the user account you used to install TLJH (which needs to have sudo rights):

```
source /opt/tljh/user/bin/activate
pip list --format=freeze > pip_pkgs.txt              # store currently installed pkgs
sudo /opt/tljh/user/bin/conda update --all
sudo /opt/tljh/user/bin/conda install python=X
sudo /opt/tljh/user/bin/pip install -r pip_pkgs.txt  # reinstall previously installed pkgs
```

Note that this is slightly different than outlined by the [instructions of TLJH](https://tljh.jupyter.org/en/latest/howto/env/user-environment.html), but at least for me those instructions didn't work properly (and the above does). Also, the reinstallation of the `pip_pkgs.txt` is important! Otherwise, the new Python version won't have all the required packages to make Jupyterhub work, and you'll get a "Cannot Spawn" error when trying to access Jupyterhub.

Alternatively, you can recompile the tests before installing the package:

```
python compile_test_modules.py
```

**Important**: if you access the server through SSH (e.g., when you're administering/configuring the server), your default Python version will *not* be the TLJH Python version, but the one that's in your path (e.g., your own Anaconda Python, if you installed one, or the system Python version). So, whenever you want to use the TLJH Python outside of the Jupyterhub interface, you need to run `source /opt/tljh/user/bin/activate` first. Also, note that this Python installation cannot be modified by regular users (for good reasons), so whenever you &mdash; as an admin user &mdash; want to modify the installation (e.g., install packages), you need to do this with `sudo`. Make sure to specify the full path to the Python program you want to use, like `sudo /opt/tljh/user/bin/pip install nilearn`, and *not* `sudo pip install nilearn`.

Alternatively, you can add the following line to your `.bashrc` file (assuming you use bash):

```
export PATH=/opt/tljh/user/bin:${PATH}
```

This will make the TLJH version of Python your default Python. Importantly, if students also use SSH (or a remote desktop client), the TLJH Python is not automatically available. To do so, add the same `export PATH=/opt/tljh/user/bin:${PATH}` line to the `/etc/skel/.bashrc` file.

After installing a new Python version, you might need to restart the Jupyterhub service by running:

```
sudo tljh-config reload hub
```

To check if everything worked, open a terminal in Jupyterhub (New &rarr; Terminal) and run `Python -V`. It should print out "Python 3.9.16".

### 5. Install `niedu`
The NI-edu course materials basically consist of two elements: the tutorial notebooks and the `niedu` Python package. The latter contains some utilities used in the notebooks and, importantly, the test that check the answers to the programming exercises. The course materials (so notebooks + `niedu`) are hosted on Github: [https://github.com/lukassnoek/NI-edu-admin](https://github.com/lukassnoek/NI-edu-admin). Importantly, you need the *admin* version of the materials, not the student version (which has the same URL, but without the `-admin` suffix). If you don't have access to this, you can contact Lukas. 

In a terminal on the server, download the course materials using `git` (`git clone https://github.com/lukassnoek/NI-edu-admin`). Then, install the `niedu` package by running the following command:

```
sudo /opt/tljh/user/bin/pip install ./NI-edu-admin
```

Note that installation of the `niedu` package by running the above command does *not* make the notebooks available to users! For this, we need to install the *nbgrader* package first (see next section).

To check your installation at this point, you can run the following command in the root of the repository:

```
python test_course_enviroment.py
```

This should print out whether the Python and `niedu` installations are as expected ("OK" or "WARNING").

### 6. Add users

It is important to remember that no one will be able to access the Jupyterhub interface unless his/her username has been added ("whitelisted") using this interface (Admin tab &rarr; Add Users) &mdash; even if this person already has a Linux (or even Jupyterhub) account on the server!

### 6. Installing/configuring *nbgrader*
Making the *nbgrader* package work is by far the trickiest part of teaching this course on Jupyterhub, but it's worth it, trust me. Grading becomes a whole lot easier and faster. The instructions below have worked for me in the past, but YMMV. 

Install the webinterface of the *nbgrader* package (including the Formgrader):

```
sudo jupyter nbextension install --sys-prefix --py nbgrader --overwrite
sudo jupyter nbextension enable --sys-prefix --py nbgrader
sudo jupyter serverextension enable --sys-prefix --py nbgrader
```

Then, we need to make sure the `nbgrader_config.py` can be found by *nbgrader*. There is a `nbgrader_config` file in the root of the `NI-edu-admin` repository. Uncomment and set the following settings:

- `c.CourseDirectory.course_id` (either "fMRI-introduction" or "fMRI-pattern-analysis")
- `c.ExecutePreprocessor.timeout` (I set it to `600`, because some exercises take a long time to run)

Then, copy this file to the following three locations (yes, you need to do all three):

1. The directory with the course materials (either `fMRI-introduction` or `fMRI-pattern-analysis`);
2. The `~/.jupyter` directory of your account (needed for the formgrader); 
3. The `/opt/tljh/user/etc/jupyter` directory (needed for fetching/submitting)

Then, reload TLJH (`sudo tljh-config reload`) and log in again. You should now be able to open the formgrader and see the list with notebooks per week (e.g., `week_1`, `week_2`, etc.). If it doesn't show, you can try restarting the hub from the Jupyterhub interface (Control Panel &rarr; Admin &rarr; Stop All &rarr; Shutdown Hub) and try again.

Lastly, you need to create and configure the "exchange" directory, which is the directory on the server that the released assignments are copied to and where the submitted assignments appear. The default directory is `/srv/nbgrader/exchange`. To create this directory and make it accessible by everyone, run the following two commands:

```
sudo mkdir -p /srv/nbgrader/exchange
sudo chmod ugo+rw /srv/nbgrader/exchange
```

Now, you should be able to release the assignment and students should be able to fetch them. Double-check this by generating and releasing an assignment and, in the "Assignments" tab in the Jupyter interface, trying to fetch the assignment.

Lastly, you need to add students to the database. Personally, I do that programatically using the command line interface of the *nbgrader* package but you can also do this manually in the Formgrader. Note: **you don't have to create the Linux accounts yourself!** This is handles by the Jupyterhub interface. 

:::{warning}
Important: when adding users to the database, make sure you enter their Linux account name in the "Student ID" field (e.g., `jupyter-nim-01`), _not_ their Jupyterhub ID (e.g., `nim-01`). This is important because `nbgrader` only "knows" about the Linux accounts, not the Jupyterhub users. 
:::

### 7. Enable SSH
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

Try reinstalling nbgrader (`sudo /opt/tljh/user/bin/pip install -U nbgrader`), reinstall the nbextension and serverextension, and reload the hub (`sudo tljh-config reload hub`).

### Letsencrypt cannot renew the certificates

Letsencrypt renews certificates using a test that uses port 80. At the UvA, we don't allow connections to this port, so the automatic renewal after 3 months will fail. To renew the certificates, temporarily open up port 80 (`sudo ufw allow 80`), run `sudo tljh-config reload proxy`, and close the port again (run `sudo ufw delete allow 80`).

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

### Jupyterhub launches JupyterLab, but I want the classic interface

Create a `*.py` file (e.g., `classic.py`) and save it in `/opt/tljh/config/jupyterhub_config.d/`. In this Python file, add a single line with:
`c.Spawner.default_url = '/tree'`

### Renewal or initial validation of SSL certificate doesn't work

It might be the case that port 80 is behind a firewall (which you cannot open up). In this situation,
you need to make sure Letsencrypt (via Traefik) uses a different verification protocol. To do so,
change the `/opt/tljh/state/traefik.toml` file as follows:

* Remove the lines with `[acme.httpChallenge]` and `entryPoint = "http"`
* Add a new line with `[acme.tlsChallenge]`

Then, instead of running `sudo tljh-config reload proxy` (which will overwrite the `traefik.toml` file), run  `systemctl restart traefik`. This will attempt the certificate renewal again. Afterwards, JupyterHub should be available via HTTPS.
