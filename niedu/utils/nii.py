import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from glob import glob
from nilearn.glm.first_level.hemodynamic_models import glover_hrf, glover_time_derivative
from scipy.interpolate import interp1d
from scipy.stats import pearsonr
from scipy.linalg import toeplitz
from scipy.ndimage import label
from IPython.display import clear_output
from time import sleep
from numpy.linalg import inv


### week 1, 2 ###
def simulate_signal(onsets, conditions, TR=2, duration=None, icept=0, params_canon=None, params_tderiv=None,
                    params_deriv1=None, phi=None, std_noise=1, osf=100, rnd_seed=None, plot=True):
    """ Simulates a somewhat realistic voxel signal with an associated design matrix. """
    if rnd_seed is not None:
        np.random.seed(rnd_seed)
    
    conds = sorted(np.unique(conditions))
    P = len(conds)
    
    if duration is None:
        duration = np.max(onsets) + 30
    
    if params_canon is None:
        params_canon = np.zeros(P)

    # TMP FIX
    params_tderiv = params_deriv1
    
    if params_tderiv is None:
        params_tderiv = np.zeros(P)

    X = np.zeros((duration * osf, P))
    for ons, con in zip(onsets, conditions):
        X[int(ons * osf), conds.index(con)] = 1
        
    hrf = glover_hrf(tr=1, oversampling=osf)
    hrf_d = glover_time_derivative(tr=1, oversampling=osf)

    t_orig = np.arange(0, duration, 1 / osf)
    t_new = np.arange(0, duration, TR)
    
    Xconv = np.zeros((t_orig.size, P * 2))
    idx = 0
    for i, this_hrf in enumerate([hrf, hrf_d]):
        this_hrf /= this_hrf.max()
        for ii in range(P):
            Xconv[:, idx] = np.convolve(X[:, ii], this_hrf)[:t_orig.size]  
            idx += 1
    
    Xconv = np.c_[np.ones(Xconv.shape[0]), Xconv]
    params = np.r_[icept, params_canon, params_tderiv]
    y = Xconv @ params
    
    resampler = interp1d(t_orig, y)
    y = resampler(t_new)       
    
    if phi is None:
        noise_cov = std_noise ** 2 * np.eye(y.size)
    else:
        noise_cov = std_noise ** 2 * phi ** toeplitz(np.arange(y.size))
    
    y = y + np.random.multivariate_normal(np.zeros(y.size), noise_cov)

    Xconv_ds = np.zeros((t_new.size, Xconv.shape[1]))
    for i in range(Xconv.shape[1]):
        resampler = interp1d(t_orig, Xconv[:, i])
        Xconv_ds[:, i] = resampler(t_new)
    
    est_betas = np.linalg.lstsq(Xconv_ds, y, rcond=None)[0]
    if plot:
        plt.figure(figsize=(15, 5))
        plt.plot(y)
        plt.plot(Xconv_ds @ est_betas)
        plt.xlim(0, y.size)
        plt.legend(['y', 'y-hat'])
        plt.show()

    return y, Xconv_ds


""" The example_voxel_signal.npy data (from week 2) was generated as follows:

onsets_squares = np.array([10, 110, 210, 310, 410, 510, 610, 710], dtype=int)
onsets_circles = np.array([60, 160, 260, 360, 460, 560, 660, 760], dtype=int)

y, X = simulate_signal(
    np.r_[onsets_squares, onsets_circles],
    ['squares'] * 8 + ['circles'] * 8,
    duration=800,
    TR=2,
    icept=1000,
    params_canon=[10, 7],
    params_deriv1=[6, 0],
    std_noise=2,
    rnd_seed=41,
    plot=True
)
np.save('example_voxel_signal.npy', y)

"""

def plot_signal_and_predicted_signal(y, X, x_lim=None, y_lim=None):
    """ Plots a signal and its GLM prediction. """
    des = np.hstack((np.ones((y.size, 1)), X))
    betas_simple = np.linalg.lstsq(des, y, rcond=None)[0]
    plt.figure(figsize=(15, 5))
    plt.plot(y)
    plt.plot(des @ betas_simple, lw=2)
    plt.xlabel('Time (in volumes)', fontsize=15)
    plt.ylabel('Activity (A.U.)', fontsize=15)
    
    if x_lim is not None:
        plt.xlim(x_lim)
    
    if y_lim is not None:
        plt.ylim(y_lim)
    
    plt.legend(['True signal', 'Predicted signal'], loc='upper right', fontsize=15)
    plt.title("Signal and predicted signal", fontsize=25)
    plt.grid()
    plt.show()
    
    
def plot_signal_and_predicted_signal_zoom(y, X, x_lim, y_lim, plot_params=True):
    """ Same as previous function, but zoomed in. """
    des = np.hstack((np.ones((y.size, 1)), X))
    betas_simple = np.linalg.lstsq(des, y, rcond=None)[0]
    yhat = des @ betas_simple
    plt.figure(figsize=(15, 5))
    plt.plot(y)
    plt.plot(yhat, lw=2)
    plt.xlim(x_lim)
    plt.ylim(y_lim)
    plt.xlabel('Time (in volumes)', fontsize=20)
    plt.ylabel('Activity (A.U.)', fontsize=20)
    
    if plot_params:
        xmid = (x_lim[1] + x_lim[0]) // 2
        plt.text(xmid, y_lim[0] + (betas_simple[0] - y_lim[0]) // 2, r"$\hat{\beta}_{intercept}$", fontsize=15)
        plt.arrow(xmid, y_lim[0], 0, betas_simple[0] - y_lim[0], head_width=0.3,
                  length_includes_head=True, color='k')

        for t in np.where(yhat[x_lim[0]:x_lim[1]] == yhat.max())[0]:
            t += x_lim[0]
            plt.arrow(t, betas_simple[0], 0, betas_simple[1], head_width=0.3,
                      length_includes_head=True, color='k')
            plt.text(t, betas_simple[0] + betas_simple[1], r"$\hat{\beta}_{1}$", fontsize=15, ha='center')
        
    plt.legend(['True signal', 'Predicted signal'], fontsize=15, loc='upper right')
    plt.show()


### week 3 ###
def calculate_stats_for_iq_income_dataset(iq_income_data, which='lowvar'):
    
    if which == 'lowvar':
        X, y = iq_income_data['X_lv'], iq_income_data['y_lv']
    else:
        X, y = iq_income_data['X_hv'], iq_income_data['y_hv']
        
    contrast = np.array([0, 1])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    y_hat = X.dot(beta)
    mse = ((y - y_hat) ** 2).mean()
    des_var = contrast.dot(np.linalg.pinv(X.T.dot(X))).dot(contrast.T)
    sse_df = ((y - y_hat) ** 2).sum() / (X.shape[0] - X.shape[1])
    se = np.sqrt(sse_df * des_var)
    tval = contrast.dot(beta) / se
    return beta, mse, tval


def calc_eff(N, X, c):
    X = np.hstack((np.ones((N, 1)), X))
    dvar = []
    for i in range(c.shape[0]):
        dvar.append(c[i, :].dot(np.linalg.pinv(X.T.dot(X))).dot(c[i, :].T))
    eff = c.shape[0] / sum(dvar)

    return eff, X


### week 4 ###
from scipy.ndimage import affine_transform
from numpy.linalg import inv


def create_sine_wave(timepoints, frequency=1,amplitude=1, phase=0):
    return amplitude * np.sin(2 * np.pi * frequency * timepoints + phase)


def add_motion_to_vols(vols):
    
    new_vols = np.zeros_like(vols)
    for i in range(new_vols.shape[-1]):
        rot = np.random.uniform(-2, 2, 3)
        trans = np.random.uniform(-0.1, 0.1, 3)
        rot_mat = get_rotation_matrix(*rot)
        trans_mat = get_translation_matrix(*trans)
        center = np.eye(4)
        center[:, -1] = np.r_[np.array(vols.shape[:3]) // 2 - 0.5, 1]
        affine = trans_mat @ center @ rot_mat @ inv(center)
        new_vols[:, :, :, i] = affine_transform(vols[:, :, :, i], matrix=inv(affine))
    return new_vols


def animate_volumes(vols, idx=25, axis=2, show_until=None, to_sleep=0.5, **kwargs):
    if show_until is None:
        show_until = vols.shape[-1]
    
    vols = np.take(vols, idx, axis)
    for i in range(show_until):
        plt.figure(figsize=(8, 8))
        plt.imshow(vols[:, :, i], cmap='gray', **kwargs)
        plt.title("Volume nr. %i" % i, fontsize=(25))
        plt.axis('off')
        plt.show()
        sleep(to_sleep)
        clear_output(wait=True)


def get_rotation_matrix(x=0, y=0, z=0):
    """ Computes the rotation matrix.
    
    Parameters
    ----------
    x : float
        Rotation in the x (first) dimension in degrees
    y : float
        Rotation in the y (second) dimension in degrees
    z : float
        Rotation in the z (third) dimension in degrees
    
    Returns
    -------
    rot_mat : numpy ndarray
        Numpy array of shape 4 x 4
    """
    
    x = np.deg2rad(x)
    y = np.deg2rad(y)
    z = np.deg2rad(z)
    
    rot_roll = np.array([
        [1, 0, 0, 0],
        [0, np.cos(x), -np.sin(x), 0],
        [0, np.sin(x), np.cos(x), 0],
        [0, 0, 0, 1]
    ])

    rot_pitch = np.array([
        [np.cos(y), 0, np.sin(y), 0],
        [0, 1, 0, 0],
        [-np.sin(y), 0, np.cos(y), 0],
        [0, 0, 0, 1]
    ])

    rot_yaw = np.array([
        [np.cos(z), -np.sin(z), 0, 0],
        [np.sin(z), np.cos(z), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    rot_mat = rot_roll @ rot_pitch @ rot_yaw
    return rot_mat


def get_translation_matrix(x=0, y=0, z=0):
    """ Computes the translation matrix.
    
    Parameters
    ----------
    x : float
        Translation in the x (first) dimension in voxels
    y : float
        Rotation in the y (second) dimension in voxels
    z : float
        Rotation in the z (third) dimension in voxels
    
    Returns
    -------
    trans_mat : numpy ndarray
        Numpy array of shape 4 x 4
    """
    
    trans_mat = np.eye(4)
    trans_mat[:, -1] = [x, y, z, 1]
    return trans_mat


### NOTE SPIKE PRED
"""
pred = np.zeros(500)
pred[::50] = 1
hrf = glover_hrf(tr=1, oversampling=1)
pred = np.convolve(pred, hrf)[:pred.size, np.newaxis]
spike_sig = pred.squeeze() + np.random.normal(1000, 0.2, pred.size)
all_sig = np.random.normal(0, 0.1, size=pred.size) + np.random.normal(1000, 0.2, ((10, 10, 10, pred.size)))
all_sig[5, 5, 5, :] = spike_sig
all_sig[:, :, :, 99] += 0.4
all_sig[:, :, :, 100] -= 0.4

all_sig[:, :, :, 299] += 0.4
all_sig[:, :, :, 300] -= 0.4

rmssd = np.sqrt(np.mean((all_sig[:, :, :, 1:] - np.diff(all_sig, axis=-1)) ** 2, axis=(0, 1, 2)))
np.savez('spike_data.npz', all_sig=all_sig, pred=pred)
"""

### For posterity
def resample2_image(image, trans_mat, rot_mat):
    """ Resamples an image given a translation and rotation matrix.
    
    Parameters
    ----------
    image : numpy array
        A 3D numpy array with image data
    trans_mat : numpy array
        A numpy array of shape 4 x 4
    rot_mat : numpy array
        A numpy array of shape 4 x 4
    
    Returns
    -------
    image_reg : numpy array
        A transformed 3D numpy array
    """
    
    # We need to rotate around the origin, not (0, 0), so
    # add a "center" translation
    center = np.eye(4)
    center[:3, -1] = np.array(image.shape) // 2 - 0.5
    A = center @ rot_mat @ trans_mat @ inv(center)
    ### WHYYYYY do I have to switch rot and trans here?
    
    # affine_transform does "pull" resampling by default, so
    # we need the inverse of A
    image_corr = affine_transform(image, matrix=np.linalg.inv(A))
    
    return image_corr

""" How the signal (y) for the last todo of week 4 was made
motion_params = np.loadtxt('func_motion_pars.txt')
N = motion_params.shape[0]
pred = np.zeros(N)
onsets = np.arange(0, N, 40)
pred[onsets.astype(int)] = 1
hrf = glover_hrf(tr=1, oversampling=1)
hrf /= hrf.max()
pred = np.convolve(pred, hrf)[:N]

motion_params[:, -1] += (pred * 0.1)
motion_params[:, -2] -= (pred * 0.1)

betas = np.concatenate((np.array([1000, 5]), np.random.uniform(-2, 2, 6)))
X = np.c_[np.ones(N), pred, motion_params]
y = X @ betas + np.random.normal(0, 5, size=N)

np.savetxt('func_motion_pars_new.txt', motion_params)
np.savez('data_motion_filtering.npz', X=np.c_[np.ones(pred.size), pred], sig=y)
"""

def compute_tvalue(X, y, c):
    # Hardcode some things to make sure it doesn't work for other data
    b = inv(X.T @ X) @ X.T @ y
    sigmasq = np.sum((y - X @ b) ** 2) / (40 - 2)
    dv = c @ inv(X.T @ X) @ c.T
    tvalue = (c @ b) / np.sqrt(sigmasq * dv)
    return tvalue


def rft_cluster_threshold(data, z_thresh=3, p_clust=0.05):
    """ This function implements a form of cluster-based
    RFT thresholding. It is based on a non-parametric
    simulation of cluster sizes under the null (with a 
    given smoothness and data shape).
    
    Do not use this for your own analyses. Only works for
    the exact data (smoothness) of the simulation data from
    week 6.
    """
    
    clust = np.load('clust_size_dist_data.npz')
    ms, zx = clust['dist'], clust['zx']

    z_idx = np.abs(zx - z_thresh).argmin()
    mask = np.zeros(data.shape, dtype=bool)
    clustered = label(data > z_thresh)[0]
    cluster_ids = np.unique(clustered)[1:]
    for cid in cluster_ids:
        clust_idx = clustered == cid
        c_size = np.sum(clust_idx)
        pval = (np.sum(ms[:, z_idx] > c_size) + 1) / (ms.shape[0] + 1)
        if pval <= p_clust:
            mask[clust_idx] = True
            
    return mask
