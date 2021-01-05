set -e

fmriprep-docker $PWD/bids $PWD/bids/derivatives --participant-label 03 -i poldracklab/fmriprep:20.1.1 --output-spaces T1w MNI152NLin2009cAsym --fs-license-file /usr/local/freesurfer/license.txt
