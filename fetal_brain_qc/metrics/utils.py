# FetMRQC: Quality control for fetal brain MRI
#
# Copyright 2023 Medical Image Analysis Laboratory (MIAL)
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import numpy as np
import skimage


def normalized_cross_correlation(x, x_ref):
    """
    Compute normalized cross correlation (symmetric).

    Original code from https://github.com/gift-surg/NSoL/blob/master/nsol/similarity_measures.py

    Input
    -----
    x:
        numpy data array
    x_ref:
        reference numpy data array
    Output
    ------
    Normalized cross correlation as scalar value between -1 and 1
    """
    if x.shape != x_ref.shape:
        raise ValueError("Input data shapes do not match")

    ncc = np.sum((x - x.mean()) * (x_ref - x_ref.mean()))
    ncc /= float(x.size * x.std(ddof=1) * x_ref.std(ddof=1))

    return ncc


def shannon_entropy(x, bins=100):
    """
    Compute Shannon entropy
    Shannon entropy H(X) = - sum p(x) * ln(p(x))
    See     Pluim, J.P.W., Maintz, J.B.A. & Viergever, M.A., 2003.
            Mutual-information-based registration of medical images: a
            survey. IEEE Transactions on Medical Imaging, 22(8), pp.986-1004.
    Original code from https://github.com/gift-surg/NSoL/blob/master/nsol/similarity_measures.py

    Input
    -----
    x:     numpy data array
    bins:  number of bins for histogram, int

    Output
    ------
    Shannon entropy as scalar value in [0, log_b(n)]
    """
    # histogram is computed over flattened array
    hist, bin_edges = np.histogram(x, bins=bins)

    # Compute probabilities
    prob = hist / float(np.sum(hist))

    entropy = -sum([p * np.log(p) for p in prob.flatten() if p != 0])

    return entropy


def joint_entropy(x, x_ref, bins=100):
    """
    Compute joint entropy (symmetric)

    Joint entropy H(X,Y) = - sum p(x,y) * ln(p(x,y))
    See      Pluim, J.P.W., Maintz, J.B.A. & Viergever, M.A., 2003.
             Mutual-information-based registration of medical images: a
             survey. IEEE Transactions on Medical Imaging, 22(8), pp.986-1004.
    Date:    2017-08-04 10:35:18+0100

    Input
    -----
    x:      numpy data array
    x_ref:  reference numpy data array
    bins:   number of bins for histogram, sequence or int

    Output
    ------
    Joint entropy as scalar value >=0

    Original code from https://github.com/gift-surg/NSoL/blob/master/nsol/similarity_measures.py
    """

    hist, x_edges, y_edges = np.histogram2d(
        x.flatten(), x_ref.flatten(), bins=bins
    )

    # Compute probabilities
    prob = hist / float(np.sum(hist))

    jentropy = -sum([p * np.log(p) for p in prob.flatten() if p != 0])
    return jentropy


def mutual_information(x, x_ref, bins=100):
    """
    Compute mutual information (symmetric)

    MI(X,Y) = - sum p(x,y) * ln( p(x,y) / (p(x) * p(y)) ) = H(X) + H(Y) - H(X,Y)
    See      Pluim, J.P.W., Maintz, J.B.A. & Viergever, M.A., 2003.
             Mutual-information-based registration of medical images: a
             survey. IEEE Transactions on Medical Imaging, 22(8), pp.986-1004.
    See      Skouson, M.B., Quji Guo & Zhi-Pei Liang, 2001. A bound on mutual
             information for image registration. IEEE Transactions on Medical
             Imaging, 20(8), pp.843-846.
    Date:    2017-08-04 10:40:35+0100

    Input
    -----
    x:      numpy data array
    x_ref:  reference numpy data array
    bins:   number of bins for histogram, sequence or int

    Output
    ------
    Mutual information as scalar value >= 0 with upper bound as in Skouson2001

    Original code from https://github.com/gift-surg/NSoL/blob/master/nsol/similarity_measures.py
    """
    mi = shannon_entropy(x, bins=bins)
    mi += shannon_entropy(x_ref, bins=bins)
    mi -= joint_entropy(x, x_ref, bins=bins)
    return mi


def normalized_mutual_information(x, x_ref, bins=100):
    """
    Compute mutual information (symmetric)

    NMI(X,Y) = H(X) + H(Y) / H(X,Y)
    See         Pluim, J.P.W., Maintz, J.B.A. & Viergever, M.A., 2003.
                Mutual-information-based registration of medical images: a
                survey. IEEE Transactions on Medical Imaging, 22(8), pp.986-1004.
    Date:       2017-08-04 10:40:35+0100

    Input
    -----
    x:      numpy data array
    x_ref:  reference numpy data array
    bins:   number of bins for histogram, sequence or int

    Output
    ------
    Normalized mutual information as scalar value >= 0

    Original code from https://github.com/gift-surg/NSoL/blob/master/nsol/similarity_measures.py
    """
    nmi = shannon_entropy(x, bins=bins)
    nmi += shannon_entropy(x_ref, bins=bins)
    nmi /= joint_entropy(x, x_ref, bins=bins)
    return nmi


def psnr(x, x_ref, datarange=None):
    if not datarange:
        datarange = int(np.amax(x_ref) - min(np.amin(x), np.amin(x_ref)))

    if sum(abs(x - x_ref)) < 1e-13:
        # Avoiding to compute the psnr on exactly the same slices.
        return np.nan
    psnr = skimage.metrics.peak_signal_noise_ratio(
        x, x_ref, data_range=datarange
    )
    return psnr


def nrmse(x, x_ref):
    return skimage.metrics.normalized_root_mse(x, x_ref)


def rmse(x, x_ref):
    return np.sqrt(skimage.metrics.mean_squared_error(x, x_ref))


def mae(x, x_ref):
    return np.mean(abs(x - x_ref))


def nmae(x, x_ref):
    return mae(x, x_ref) / np.mean(np.abs(x_ref))


def ssim(x, x_ref, mask=None, datarange=None):
    if not datarange:
        datarange = int(np.amax(x_ref) - min(np.amin(x), np.amin(x_ref)))

    # SSIM
    ssim = skimage.metrics.structural_similarity(
        x_ref,
        x,
        data_range=datarange,
        full=True,
    )

    def pick_ssim(ssim, mask):
        """Pick the SSIM output:
        1- If masked input, take the full SSIM on the masked input
        2- Else, return the average SSIM
        """
        if mask is None:
            return ssim[0]
        else:
            return ssim[1][mask > 0].mean()

    return pick_ssim(ssim, mask)
