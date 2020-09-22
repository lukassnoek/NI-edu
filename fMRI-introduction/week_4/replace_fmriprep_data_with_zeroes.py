import numpy as np
import nibabel as nib
from glob import glob

niis = sorted(glob('bids/derivatives/fmriprep/sub-03/*/*.nii.gz'))
for nii in niis:
    img = nib.load(nii)
    img_new = nib.Nifti1Image(np.zeros(img.shape), affine=img.affine)
    img_new.to_filename(nii)
