import os.path as op
import numpy as np


def generate_labels(con, N_per_con, p=[0.7, 0.3]):
    """ Generates slightly correlated labels. """
    labels = np.repeat(con, N_per_con)
    seq = []
    for i in range(labels.size):
        idx = np.arange(labels.size)
        if not seq:
            c = np.random.choice(idx)
        else:
            p_arr = np.zeros(idx.size)
            pm = p[0] if seq[-1] == con[0] else p[1]
            nm, nf = (labels == con[0]).sum(), (labels == [con[1]]).sum()
            if nm == 0 or nf == 0:
                p_arr = None
            else:
                p_arr[labels == con[0]] = pm / nm
                p_arr[labels == con[1]] = (1 - pm) / nf

            c = np.random.choice(idx, p=p_arr)

        seq.append(labels[idx[c]])
        labels = np.delete(labels, idx[c])
    return seq


def filter_pattern_drift(R, deg=8):
    """ Filters out 'pattern drif' using a 
    polynomial basis set. 
    
    Parameters
    ----------
    R : numpy array
        A 2D numpy array with patterns (NxK)
    deg : int
        Degree of polynomial basis set

    Returns
    -------
    R_filt : numpy array
        Filtered pattern array
    """
    # Define initial regressor
    x = np.arange(R.shape[0])
    
    # Create basis set + fit on R
    b = np.polyfit(x, R, deg=deg)
    
    # Use parameters (b) to evaluate basis set (x @ b)
    low_freq = np.polyval(b, x[:, np.newaxis])
    
    # Remove estimated low frequencies from data (R)
    R_filt = R - low_freq
    return R_filt