""" Downloads the necessary data from Openneuro. """
import yaml
import click
import subprocess
import os.path as op


@click.command()
@click.argument('save_dir', type=click.Path(exists=False))
@click.option('--course', type=click.Choice(['introduction', 'pattern-analysis', 'both'], help='Which course?')
def main(save_dir, course):

    if op.isdir(save_dir):
        raise ValueError(f"The directory {save_dir} already exists; please choose another save directory!")

    try:
        import awscli
    except:
        msg = ("Please install the Python package `awscli` using pip:\n\n"
            "pip install awscli\n\n"
            "Then, run this script again.")
        raise ValueError(msg)

    size = {'introduction': '8GB', 'pattern-analysis': '10GB', 'both': '18GB'}

    msg = (f"WARNING: this script will download {size[course]} and save it here: "
           f"{op.abspath(save_dir)}\n"
           "Do you want to continue [y/n]? ")
    resp = input(msg)
    if resp in ['n', 'N', 'no', 'NO', 'No']:
        exit()

    aws_bucket = {'introduction': 'ds003349', 'pattern-analysis': 'ds000000'}
    to_loop = [course] if course != 'both' else ['introduction', 'pattern-analysis']
    for c in to_loop:
        if course == 'both':
            this_save_dir = op.join(save_dir, c)
        else:
            this_save_dir = save_dir

        cmd = f"aws s3 sync --no-sign-request s3://openneuro.org/{aws_bucket[c]} {this_save_dir}/"
        return_code = subprocess.call(cmd.split(' '))

        if return_code == 0:
            print(f"\n\nDownload successful for data for the '{c}' course!")
        else:
            print(f"\n\nSomething went wrong when downloading data for the '{c}' course ...")
            
        # Add data path to course settings
        with open('course_settings.yml', 'r') as stream:
            settings = yaml.safe_load(stream)
    
        settings['data_dir'][c] = this_save_dir
        with open('course_settings.yml', 'w') as outfile:
            yaml.dump(settings, outfile, default_flow_style=False)


if __name__ == '__main__':
    main()