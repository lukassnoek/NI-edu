# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"></ul></div>

import os.path as op
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import seaborn as sns
from scipy.spatial.distance import squareform
from scipy.stats import rankdata


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


def show_rankRDM(rdm, ax = None, label=None):
    sns.set_context('poster')
    if ax == None:
        plt.figure()
        plt.imshow(squareform(rankdata(squareform(rdm))))
        plt.title(label)
        plt.axis('off')
        plt.show()
    else:
        ax.imshow(squareform(rankdata(squareform(rdm))))
        ax.set_title(label)
        ax.axis('off')

        return ax


# Bootstrapping
def corr_variability(mean_rdm_vec, feature_rdm_vec, iterations=100):

    rdm_corr_boots = []
    for i in range(iterations):
        if i%10 == 0:
            print('Iteration: ' + str(i) )
        # Create a random index that respects the structure of an rdm.
        sample = np.random.choice(mean_rdm_vec.shape[0],mean_rdm_vec.shape[0],replace=True) # note that now replace is True

        # Subsample from both the reference and the feature RDM
        mean_rdm_sample = mean_rdm_vec[sample] 
        feature_rdm_sample = feature_rdm_vec[sample] 

        # correlating with neural similarty matrix
        rdm_corr_boots.append(spearmanr(mean_rdm_sample, feature_rdm_sample)[0])

    return rdm_corr_boots



# Statistical significance
def corr_nullDist(mean_rdm, feature_rdm_vec, iterations=100):
    rdm_corr_null = []
    for i in range(iterations):
        if i%10 == 0:
            print('Iteration: ' + str(i) )
        # Create a random index that respects the structure of an rdm.
        shuffle = np.random.choice(mean_rdm.shape[0],mean_rdm.shape[0],replace=False)

        # shuffle RDM consistently for both dims
        mean_rdm_shuffle = mean_rdm[shuffle,:] # rows
        mean_rdm_shuffle = mean_rdm_shuffle[:,shuffle] # columns

        # correlating with neural similarty matrix
        rdm_corr_null.append(spearmanr(squareform(mean_rdm_shuffle), feature_rdm_vec)[0])
    return rdm_corr_null


