import os
import yaml
import os.path as op
import numpy as np
import matplotlib.pyplot as plt

here = op.dirname(__file__)


def get_data_dir(course='introduction'):
    """ Returns the course's data directory.
    
    Parameters
    ----------
    course : str
        Which course do you want the data for? (introduction/pattern-analysis)

    Returns
    -------
    data_dir : str
        Absolute path to data directory
    """
    
    courses = ['introduction', 'pattern-analysis']
    if course not in courses:
        raise ValueError(f"Please choose course from {courses}!")

    cs = op.join(here, 'data', 'course_settings.yml')
    with open(cs, 'r') as f_in:
        settings = yaml.safe_load(f_in)

    data_dir = settings['data_dir'][course]
    if not op.isdir(data_dir):
        print(f"WARNING: data dir {data_dir} does not exist!"
              "Please adjust the course_settings.yml file!")
    
    return data_dir


def show_directory_tree(directory, ignore=None):
    """ Prints directory tree.
    
    directory : str
        Path to directory to print
    ignore : str
        Files with this substring will not be printed
    """
    for root, _, files in os.walk(directory):
        
        files = sorted(files)
        if ignore is not None:
            files = [f for f in files if ignore not in f]

        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def plot_ortho_slices(img):
    """ Plots 3 orthogonal slices (in 3 directions).
    
    Parameters
    ----------
    img : numpy ndarray
        Array with 3 dimensions
    fig : matplotlib Figure
        Figure to plot on
        
    Returns
    -------
    fig : Figure
    ax : axes
    """
    sh = img.shape
    
    fig, axes = plt.subplots(ncols=3, figsize=(15, 10))
    for i in range(3):
        tmp = np.take(img, sh[i] // 2, axis=i)
        axes[i].imshow(tmp.T, origin='lower', cmap='gray')
        axes[i].axis('off')

    fig.tight_layout()
    fig.show()
    return fig, axes


def convert_grades_to_canvas_format(csv):

    df = pd.read_csv(csv).loc[:, [
        'assignment',
        'first_name',
        'last_name',
        'score',
        'max_score'
    ]]

    df = df.dropna(how='any', axis=0)
    df['final_score'] = df['score'] / df['max_score']
    df = df.loc[df['final_score'] != 0, :]
    df.loc[:, 'assignment'] = 'lab_' + df.loc[:, 'assignment']

    df = df.pivot(columns='assignment', values='final_score', index='last_name')
    df = df.reset_index()
    df.iloc[:, 1:] = df.iloc[:, 1:].round(2) * 10
    df.to_csv(csv.replace('.csv', '_fixed.csv'), index=None)
