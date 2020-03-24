import os
import sys
import click
import subprocess
import shutil
import pandas as pd
import os.path as op
from glob import glob

REPO_ROOT = op.dirname(op.dirname(__file__))

def niedu_download_data():
    print("Downloading")

def niedu_enable_nbgrader():
    cmds = [
        "jupyter nbextension install --sys-prefix --py nbgrader --overwrite",
        "jupyter nbextension enable --sys-prefix --py nbgrader",
        "jupyter serverextension enable --sys-prefix --py nbgrader"
    ]
    for cmd in cmds:
        subprocess.run(cmd.split(' '))

@click.command()
@click.option("--user", help="username to use")
@click.option("--passwd", help="password to use")
def niedu_create_single_user(user, passwd):
    cmd = f'sudo adduser -q --gecos "" --disabled-password {user}'
    print(f"Creating user {user} with password {passwd} ...")
    subprocess.run(cmd, shell=True)
    cmd = f"echo '{user}:{passwd}' | sudo chpasswd"
    subprocess.run(cmd, shell=True)


@click.command()
@click.option('--user', help="Username")
@click.option('--fsldir', help="Location of FSL directory")
def niedu_add_fsl_path_to_bashrc_api(user, fsldir):
    niedu_add_fsl_path_to_bashrc(user, fsldir=None)

def niedu_add_fsl_path_to_bashrc(user, fsldir=None):

    if fsldir is None:
        print("Retrieving FSL dir from $FSLDIR env variable ...")
        fsldir = os.environ.get('FSLDIR')
        if fsldir is None:
            msg = ("You didn't supply the FSL dir (--fsldir) and couldn't find it in the "
                   "environment variables.")
            raise ValueError(msg)

    bashrc = f'/home/{user}/.bashrc'
    if not op.isfile(bashrc):
        raise ValueError(f"The {bashrc} file doesn't exist!")

    to_add = [
        f"source {fsldir}/etc/fslconf/fsl.sh",
        f"FSLDIR={fsldir}",
        f"PATH={fsldir}/bin:$PATH",
        "export FSLDIR PATH"
    ]
    
    with open(bashrc, 'r') as f_in:
        lines = f_in.readlines()

    for l in to_add:
        if l not in lines:
            lines.append(l)

    with open(bashrc, 'w') as f_out:
        for l in lines:
            f_out.write(l + '\n')


@click.command()
@click.option("--prefix", default="nim_", help="Prefix for student homes")
def niedu_delete_users(prefix='nim_'):

    homes = sorted(glob(f'/home/{prefix}*'))
    print(f"Found the following homes: {homes}")
    
    while True:
        ans = input(f"Want to remove {len(homes)}? [y, n]")
        if ans in ['y', 'n']:
            break
        else:
            print("Please answer either 'y' or 'n'!\n")
    
    if ans == 'n':
        print("Exiting ...")
        return

    for home in homes:
        cmd = f'userdel {op.basename(home)} -rf'
        print(f"Removing {home} ...")
        subprocess.call(cmd, shell=True)
    

@click.command()
@click.option("--logins", default="users.csv", help="File with users")
@click.option("--fsldir", default=None, help="FSL directory")
def niedu_create_users(logins, fsldir=None):
    
    if not op.isfile(logins):
        raise ValueError(f"Cannot find file {logins}!")

    sep = '\t' if logins.split('.')[-1] == 'tsv' else ','
    login_data = pd.read_csv(logins, sep=sep)

    for _, row in login_data.iterrows():
        username = row['username']
        firstname, lastname = row['first_name'], row['last_name']
        password = row['password']
        lms = row['lms']
        if not op.isdir(f'/home/{username}'):
            print(f'Creating user {username} with password {password} ...')
            cmd = f'adduser -q --gecos "" --disabled-password {username}'
            subprocess.run(cmd, shell=True)
            cmd = f"echo '{username}:{password}' | chpasswd"
            subprocess.run(cmd, shell=True)
            print("Appending FSL info to .bashrc ...")
            niedu_add_fsl_path_to_bashrc(username, fsldir)  # NOT YET TESTED
        else:
            print(f'User {username} already exists!')

        cmd = f"nbgrader db student add {username} --first-name \'{firstname}\' --last-name \'{lastname}\' --lms-user-id \'c{lms}\'"
        print(f"Running: {cmd}")
        subprocess.call(cmd, shell=True)
