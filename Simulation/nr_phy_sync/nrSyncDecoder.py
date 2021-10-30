from typing import Union
import numpy as np
import nrSyncSignals
import nrSSB
from pyphysim.modulators import OFDM, QPSK


def decode_pss(received_data, ssb_dim):
    """Find SSB with highest crosscorrelation to undistorted PSS available in resource grid 
    and extract N_ID_2, k_ssb and l_ssb

    Args:
        received_data ([complex, complex]): 2D resource grid in which to search for SSB
        ssb_dim (struct): SSB dimensions and nu

    Returns:
        tuple: N_ID_2, k_ssb, l_ssb
    """
    rec_pss_sym = np.array(received_data)
    nid2_candidates = np.array(
        [nrSyncSignals.pss(N_ID2=n_id2) for n_id2 in range(3)])

    corr = np.zeros(
        (3, received_data.shape[0], received_data.shape[1]), dtype=complex)

    for (i, pss_i) in enumerate(nid2_candidates):
        rgrid_mask = np.zeros(rec_pss_sym.shape, dtype=complex)
        rgrid_mask[:ssb_dim['k'], :ssb_dim['l']
                   ] += nrSSB.map_pss(pss_i, ssb_dim)

        for l in range(received_data.shape[1]):
            for k in range(received_data.shape[0]):
                corr[i, k, l] = np.multiply(
                    np.roll(
                        np.roll(rgrid_mask, l, axis=1),
                        k, axis=0),
                    rec_pss_sym.real).sum()

    return np.unravel_index(np.argmax(corr, axis=None), corr.shape)


def pss_correlate(ofdm_sym):
    '''
    todo doc
    input: 1d array with any number of carriers
    output (NID_2, k_ssb, max_correlation)
    '''
    ofdm_sym = ofdm_sym.flatten()
    corr = np.array([np.abs(np.correlate(ofdm_sym, nrSyncSignals.pss(nid2)))
                    for nid2 in range(3)], dtype=float)
    (nid2, pss_start) = np.unravel_index(np.argmax(corr), corr.shape)
    return (nid2, pss_start-56, corr[nid2, pss_start])


def pss_coarse_time_frequency_corr(fft_size: int, received_data: Union[np.ndarray, list], threshold: float, threshold_filter_down_spampling_factor: int, ret_mat: False):
    '''
    todo doccccc
    fft_size >= 240
    returns nid2, 
    '''
    # filter idxs which have avg for range of fftsize under given threshold
    can_idxs = np.array(range(len(received_data)-fft_size))
    for ind in range(0, len(can_idxs), ):
        if np.average(np.abs(received_data[ind:ind+fft_size:threshold_filter_down_spampling_factor])) < threshold:
            can_idxs[ind] = -1
    idxs = can_idxs[can_idxs != -1]

    ofdm = OFDM(fft_size, 0, fft_size)

    corr = np.ones(shape=(3, fft_size-239, len(received_data) -
                   fft_size + 1), dtype=np.float64) * np.inf

    for i_NID_2 in range(corr.shape[0]):
        pss_i_data = nrSyncSignals.pss(N_ID2=i_NID_2)
        ssb_dim = {
            'k': fft_size,
            'l': 1
        }
        pss_i = nrSSB.map_pss(pss_i_data, ssb_dim)[:, 0]
        for i_f_offs in range(corr.shape[1]):
            candidate = ofdm.modulate(  # np.fft.ifft(#
                np.roll(pss_i, i_f_offs))
            for i_t_offs in idxs:
                corr[i_NID_2, i_f_offs, i_t_offs] = np.abs(np.sum(np.square(
                    received_data[i_t_offs:i_t_offs+len(candidate)]) - np.square(candidate)))
    corr = np.divide(1, corr)
    correc = np.unravel_index(np.argmax(corr, axis=None), corr.shape)
    if ret_mat:
        return (correc, corr)
    return correc


def decode_sss(sss_data, nid2):
    """Extract N_ID_1 through crosscorrelation

    Args:
        sss_data ([complex]): unmapped SSS
        N_ID2 (int): Cell ID sector
        ssb_dim (struct): SSB dimensions and nu

    Returns:
        int: N_ID_1
    """
    sss_candidates = np.array([nrSyncSignals.sss(
        N_ID1=nid1,
        N_ID2=nid2) for nid1 in range(336)])

    corr = np.zeros(len(sss_candidates), dtype=complex)

    for i, sss_i in enumerate(sss_candidates):
        corr[i] = np.abs(np.multiply(sss_i, sss_data).sum())

    return int(np.argmax(corr, axis=None))


def decode_pbch(pbch_data: np.ndarray, L__max: int, N_ID_Cell: int, i_SSB: int):
    # get bits from complex symbols
    b = nrSyncSignals.inv_sym_qpsk(np.array(pbch_data, dtype=complex))
    # descramble that
    M_bit = len(b)
    if not M_bit == 864:
        raise ValueError('PBCH payload data must be 864 symbols')
    v = None
    if L__max == 4:
        v = i_SSB % 2**2
    else:
        v = i_SSB % 2**3

    c = nrSyncSignals.prsg((1+v) * M_bit, N_ID_Cell)
    scr = [c[i + v * M_bit] for i in range(M_bit)]

    return np.logical_xor(b, scr)
