import os
import click
import pandas as pd
import os.path as op
from glob import glob
from niedu.global_utils import get_data_dir


def create_fsl_onset_files(data_dir):
    """ Creates FSL-style onset files (tab-delimited, without headers). """
    subs = sorted(glob(op.join(data_dir, 'sub-03')))
    for sub in subs:
        # first flocBLOCKED and flocER files
        flocs = sorted(glob(op.join(sub, 'ses-*', 'func', '*floc*_events.tsv')))

        for floc in flocs:
            df = pd.read_csv(floc, sep='\t')
            conds = np.unique(df['trial_type'])
            for con in conds:
                f_out = floc.replace('_events.tsv', f'_condition-{con}_events.txt')
                #if op.isfile(f_out):
                #    continue

                tmp = df.query("trial_type == @con").copy()
                tmp.loc[:, 'weight'] = 1
                tmp.loc[:, 'duration'] = tmp.loc[:, 'duration'].round(1)
                tmp = tmp.loc[:, ['onset', 'duration', 'weight']]  # reorder
                tmp.to_csv(f_out, header=False, index=False, sep='\t')


@click.command()
@click.option('--datadir', default=None, help='Directory with data')
@click.option('--fsldir', default=None, help='FSL directory')
def api(datadir, fsldir):
 
    if datadir is None:
        datadir = get_data_dir()
    
    if not os.path.isdir(datadir):
        raise ValueError(f"Datadir {datadir} does not exist!")

    print(f"Found {datadir} with data!")
    create_fsl_onset_files(datadir)



if __name__ == '__main__':
    api()
