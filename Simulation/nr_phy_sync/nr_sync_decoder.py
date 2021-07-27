import numpy as np
from nr_phy_sync import nr_sync_signals as nrss
from nr_phy_sync import nr_ssb

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
    nid2_candidates = np.array([nrss.pss(N_ID2 = n_id2) for n_id2 in range(3)])
    
    corr = np.zeros((3, received_data.shape[0], received_data.shape[1]), dtype=complex)
    
    for (i,pss_i) in enumerate(nid2_candidates):
        rgrid_mask = np.zeros(rec_pss_sym.shape, dtype=complex)
        rgrid_mask[:ssb_dim['k'], :ssb_dim['l']] += nr_ssb.map_pss(pss_i, ssb_dim)
        
        for l in range(received_data.shape[1]):
            for k in range(received_data.shape[0]):
                corr[i, k, l] =np.multiply(
                    np.roll(
                        np.roll(rgrid_mask, l, axis=1),
                            k, axis=0),
                        rec_pss_sym.real).sum()
                    
                
    return  np.unravel_index(np.argmax(corr, axis=None), corr.shape)


def decode_sss(sss_data, nid2, ssb_dim):
    """Extract N_ID_1 through crosscorrelation

    Args:
        sss_data ([complex]): unmapped SSS
        N_ID2 (int): Cell ID sector
        ssb_dim (struct): SSB dimensions and nu

    Returns:
        int: N_ID_1
    """
    sss_candidates = np.array([nrss.sss(
        N_ID1 = nid1,
        N_ID2 = nid2) for nid1 in range(336)])
    
    corr = np.zeros(len(sss_candidates),dtype=complex)
    
    for i,sss_i in enumerate(sss_candidates):
        corr[i] = np.multiply(sss_i, sss_data).sum()
    
    return max(np.unravel_index(np.argmax(corr, axis=None), corr.shape))
