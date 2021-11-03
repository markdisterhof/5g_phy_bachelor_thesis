import numpy as np
import nrSyncSignals as nrss


def map_pss(data, ssb_dim, beta=1.):
    """Mapping of PSS within an SS/PBCH block as per

    TS 38 211 V16.2.0 (2020-07) 7.4.3.1.1

    Args:
        data : PSS data
        ssb_dim (struct) : SSB dimensions and nu
        beta (float, optional): PSS power allocation factor. Defaults to 1.0

    Raises:
        ValueError: PSS data must be 127 symbols

    Returns:
        [complex, complex]: SSB with mapped PSS
    """
    if not len(data) == 127:
        raise ValueError("PSS data must be 127 symbols")
    mask = np.zeros((ssb_dim['k'], ssb_dim['l']), dtype=complex)
    data = np.array(data) * beta
    mask[56:183, 0] = data
    return mask


def map_sss(data, ssb_dim, beta=1.):
    """Mapping of SSS within an SS/PBCH block as per

    TS 38 211 V16.2.0 (2020-07) 7.4.3.1.2

    Args:
        data : SSS data
        ssb_dim (struct) : SSB dimensions and nu
        beta (float, optional): SSS power allocation factor. Defaults to 1.0

    Raises:
        ValueError: SSS data must be 127 symbols

    Returns:
        [complex, complex]: SSB with mapped SSS
    """
    if not len(data) == 127:
        raise ValueError("sss data must be 127 symbols")
    mask = np.zeros((ssb_dim['k'], ssb_dim['l']), dtype=complex)
    data = np.array(data) * beta
    mask[56:183, 2] = data
    return mask


def map_pbch(data_pbch, data_dmrs, ssb_dim, beta_pbch=1., beta_dmrs=1.):
    """Mapping of PBCH and DM-RS within an SS/PBCH block as per

    TS 38 211 V16.2.0 (2020-07) 7.4.3.1.3

    Args:
        data_pbch ([complex]): PBCH data
        data_dmrs ([complex]): DM-RS data
        ssb_dim (struct): SSB dimensions and nu
        beta_pbch (float, optional): PBCH power allocation factor. Defaults to 1.0
        beta_dmrs (float, optional): DM-RS power allocation factor. Defaults to 1.0

    Raises:
        ValueError: data_pbch must be 432 symbols, data_dmrs must be 144 symbols

    Returns:
        [complex, complex]: SSB with mapped PBCH and DM-Rs
    """
    if not len(data_pbch) == 432 or not len(data_dmrs) == 144:
        raise ValueError(
            "pbch is always 432 symbols, dmrs is always 144 symbols")
    i_dmrs, i_pbch = 0, 0

    data_pbch = np.array(data_pbch,dtype=complex) * beta_pbch
    data_dmrs = np.array(data_dmrs,dtype=complex) * beta_dmrs
    mask = np.zeros((ssb_dim['k'], ssb_dim['l']), dtype=complex)

    for l in range(1, 4):
        k_range = range(240)
        if l == 2:
            k_range = np.concatenate((range(48), range(192, 240)))
        for k in k_range:
            
            if k % 4 == ssb_dim['nu']:
                mask[k, l] = data_dmrs[i_dmrs]
                i_dmrs += 1
            else:
                mask[k, l] = data_pbch[i_pbch]
                i_pbch += 1
    return mask


def ssb(ssb_dim, N_ID1, N_ID2, L__max, ssb_idx, pbch_data):
    """Generate SS/PBCH block 

    Args:
        ssb_dim (struct): SSB dimensions and nu
        N_ID1 (int): Cell ID group
        N_ID2 (int): Cell ID sector
        L__max (int): Maximum number of candidate SS/PBCH blocks in a half frame
        ssb_idx (int): Candidate SS/PBCH block index

    Returns:
        [complex,complex]: 
    """

    N_ID_Cell = 3 * N_ID1 + N_ID2

    ssb = np.zeros((ssb_dim['k'], ssb_dim['l']), dtype=complex)  # one ssb

    # pss mapping
    data_pss = nrss.pss(N_ID2=N_ID2)

    ssb += map_pss(data_pss, ssb_dim)

    # sss mapping
    data_sss = nrss.sss(
        N_ID1=N_ID1,
        N_ID2=N_ID2)

    ssb += map_sss(data_sss, ssb_dim)

    # pbch and dmrs mapping
    data_pbch = nrss.pbch(
        pbch_data,
        L__max,
        N_ID_Cell,
        ssb_idx)

    data_dmrs = nrss.dmrs(ssb_idx, N_ID_Cell, L__max, 0)

    ssb += map_pbch(data_pbch, data_dmrs, ssb_dim)
    return ssb


def unmap_pss(received_data: np.ndarray, ssb_dim: dict = None):
    """Unmap PSS from given resource grid

    Args:
        received_data ([complex, complex]): 2D resource grid
        ssb_dim (struct): SSB dimensions and nu 

    Returns:
        [complex]: PSS data
    """
    if ssb_dim is None:
        ssb_dim = {
            'l': 4,
            'k': 240
        }
    ssb_dim['k_offset'] = ssb_dim.get('k_offset', 0)
    ssb_dim['l_offset'] = ssb_dim.get('l_offset', 0)

    ssb_mask = np.zeros((ssb_dim['k'], ssb_dim['l']), dtype=int)
    ssb_mask += map_pss(np.ones(127), ssb_dim)
    mask_rgrid = np.zeros(received_data.shape)
    mask_rgrid[ssb_dim['k_offset']:ssb_dim['k_offset']+240,
               ssb_dim['l_offset']:ssb_dim['l_offset']+4] = ssb_mask
    return received_data[
        np.nonzero(
            np.multiply(mask_rgrid, received_data))]


def unmap_sss(received_data: np.ndarray, ssb_dim: dict = None):
    """Unmap SSS from given resource grid

    Args:
        received_data ([complex, complex]): 2D resource grid
        ssb_dim (struct): SSB dimensions and nu 

    Returns:
        [complex]: SSS data
    """
    if ssb_dim is None:
        ssb_dim = {
            'l': 4,
            'k': 240
        }
    ssb_dim['k_offset'] = ssb_dim.get('k_offset', 0)
    ssb_dim['l_offset'] = ssb_dim.get('l_offset', 0)

    ssb_mask = np.zeros((ssb_dim['k'], ssb_dim['l']), dtype=complex)
    ssb_mask += map_sss(np.ones(127, dtype=complex), ssb_dim)
    mask_rgrid = np.zeros(received_data.shape, dtype=complex)
    mask_rgrid[ssb_dim['k_offset']:ssb_dim['k_offset']+240,
               ssb_dim['l_offset']:ssb_dim['l_offset']+4] = ssb_mask
    return np.ma.masked_array(
        received_data.flatten(order='F'),
        np.logical_not(
            mask_rgrid.flatten(order='F')
        )
    ).compressed()


def unmap_pbch(received_data: np.ndarray, ssb_dim: dict = None):
    """Unmap PBCH and DM-RS from given resource grid

    Args:
        received_data ([complex, complex]): 2D resource grid
        ssb_dim (struct): SSB dimensions and nu 

    Returns:
        tuple: PBCH and DM-RS data
    """
    if ssb_dim is None:
        ssb_dim = {
            'l': 4,
            'k': 240
        }
    ssb_dim['k_offset'] = ssb_dim.get('k_offset', 0)
    ssb_dim['l_offset'] = ssb_dim.get('l_offset', 0)

    ssb_mask_pbch = np.zeros((ssb_dim['k'], ssb_dim['l']), dtype=complex)
    ssb_mask_dmrs = np.zeros((ssb_dim['k'], ssb_dim['l']), dtype=complex)

    ssb_mask_pbch += map_pbch(np.ones(432), np.zeros(144), ssb_dim)
    ssb_mask_dmrs += map_pbch(np.zeros(432), np.ones(144), ssb_dim)

    mask_rgrid_pbch = np.zeros(received_data.shape, dtype=complex)
    mask_rgrid_dmrs = np.zeros(received_data.shape, dtype=complex)

    mask_rgrid_pbch[ssb_dim['k_offset']:ssb_dim['k_offset']+240,
                    ssb_dim['l_offset']:ssb_dim['l_offset']+4] = ssb_mask_pbch
    mask_rgrid_dmrs[ssb_dim['k_offset']:ssb_dim['k_offset']+240,
                    ssb_dim['l_offset']:ssb_dim['l_offset']+4] = ssb_mask_dmrs

    # data_pbch = received_data.flatten(order='F')[np.nonzero(
    #     np.multiply(mask_rgrid_pbch, received_data).flatten(order='F'))]
    # data_dmrs = received_data.flatten(order='F')[np.nonzero(
    #     np.multiply(mask_rgrid_dmrs, received_data).flatten(order='F'))]
    data_pbch = np.ma.masked_array(
        received_data.flatten(order='F'),
        np.logical_not(
            mask_rgrid_pbch.flatten(order='F')
        )
    ).compressed()

    data_dmrs = np.ma.masked_array(
        received_data.flatten(order='F'),
        np.logical_not(
            mask_rgrid_dmrs.flatten(order='F')
        )
    ).compressed()

    return data_pbch, data_dmrs


def map_ssb(res_grid, ssb, k_offs, l_offs):
    """Place SSB in provided resource grid with offsets 

    Args:
        res_grid ([complex, complex]): 2D resource grid
        ssb ([complex, complex]): 2D SSB
        k_offs (int): Offset counted in multiples of Subcarriers
        l_offs (int): Offset counted in slots

    Returns:
        [complex, complex]: 2D resource grid
    """
    res_grid[k_offs:len(ssb)+k_offs, l_offs:len(ssb[0, :])+l_offs] = ssb
    return res_grid


def grid(n_carr=240, N_ID1=0, N_ID2=0, k_ssb=0, mu=0, f=0, shared_spectr=False, paired_spectr=False, pbch= np.random.randint(2, size=864)):
    if n_carr < 240 + k_ssb:
        raise ValueError('Provided n_carr is too small. n_carr: {0}, needed: {1}'.format(n_carr,240+k_ssb))
    


    #find N_RB 
    N_RB = int(n_carr//12)

    #gen rgrid for sync
    grid = get_sync_resource_grid_pbch(N_RB, N_ID1, N_ID2, k_ssb, mu, f, pbch, shared_spectr, paired_spectr)

    #fit grid with N_RB*12 carr into n_carr
    mask= np.zeros((n_carr,len(grid[0])), dtype=complex)
    mask[:len(grid),:len(grid[0])]= grid

    return mask


def get_sync_resource_grid_pbch(N_RB, N_ID1, N_ID2, k_ssb, mu, f, pbch_data, shared_spectr, paired_spectr):
    """Generate a complete resource grid with SSBs

    Args:
        mu (int): Numerology
        N_RB (int): number of Resource blocks 
        N_ID1 (int): cell ID group
        N_ID2 (int): cell ID sector
        f (int): center frequency of the band
        k_ssb (int): see See 38.211 7.4.3.1 
        shared_spectr (bool, optional): shared spectrum channel access. Defaults to False
        paired_spectr (bool, optional): paired spectrum operation. Defaults to False

    Returns:
        [complex, complex]: 2D ndarray representing the produced resource grid
    """

    N_ID_Cell = 3 * N_ID1 + N_ID2
    ssb_dim = {
        'l': 4,
        'k': 240,
        'nu': N_ID_Cell % 4
    }
    N_SC, N_SYMB = get_rgrid_dimensions(mu, N_RB)

    can_idxs = get_ssb_candidate_idx(mu, f, shared_spectr, paired_spectr)
    idxs = get_ssb_idxs(can_idxs, mu, shared_spectr)
    L__max = len(idxs)
    res_grid = np.zeros(shape=(N_SC, N_SYMB), dtype=complex)

    pbch_data = np.array(pbch_data)
    pbch_data.resize(L__max*864)
    pbch_data_arr = pbch_data.reshape(L__max,864)
    
    for i_ssb,idx in enumerate(idxs):
        ssb_i = ssb(ssb_dim, N_ID1, N_ID2, L__max, i_ssb, pbch_data_arr[i_ssb])
        res_grid = map_ssb(res_grid, ssb_i, k_ssb, idx)
    return res_grid


def get_rgrid_dimensions(mu, n_rb):
    """Returns number of subcarriers and number of symbols in a frame. 

    See TS 38.211 Table 4.3.2-1,
        TS 38.101-1 Table 5.3.2-1

    Args:
        mu (int): Numerology index {0,1,2,3,4}
        n_rb (int): Number of resource blocks

    Returns:
        (int, int): N_SC, N_SYMB_FRAME
    """
    N_SC_RB = 12
    N_SC = n_rb * N_SC_RB

    N_SYMB_SLOT = 14
    N_SLOTS_FRAME = 2 ** mu * 10
    N_SYMB_FRAME = N_SYMB_SLOT * N_SLOTS_FRAME

    return (N_SC, N_SYMB_FRAME)


def get_ssb_idxs(candidate_idxs, mu, shared_spectr):
    if shared_spectr:
        if (len(candidate_idxs) == 10 and mu == 0) or (len(candidate_idxs) == 20 and mu == 1):
            return candidate_idxs[:8]

    return candidate_idxs


def get_ssb_candidate_idx(mu: int, f: int, ssca=False, paired=False):
    """Compute indexes of the first symbols of the the cadidate SS/PBCH blocks
    as per 

    38.213 V16.3.0 (2020-11)

    4.1 Cell search

    Args:
        mu (int): Numerology index
        f (int): Carrier frequencies (max)
        ssca (bool, optional): shared spectrum channel access. Defaults to False.
        paired (bool, optional): paired spectrum operation. Defaults to False.

    Returns:
        [int]: Indexes of the first symbols of the the cadidate SS/PBCH blocks
    """
    n = []
    i = []
    scs = int(2**mu * 15e3)

    if scs == 15e3:
        # case A
        i = np.array([2, 8])
        if ssca:
            # shared spectrum channel access, as described in [15, TS 37.213]s
            n = np.array([0, 1, 2, 3, 4])
        elif f <= 3e9:
            n = np.array([0, 1])
        else:
            n = np.array([0, 1, 2, 3])
        n *= 14

    elif scs == 30e3 and not (ssca or paired):
        # case B
        i = np.array([4, 8, 16, 20])
        if f <= 3e9:
            n = np.array([0])
        else:
            n = np.array([0, 1])
        n *= 28

    elif scs == 30e3 and (ssca or paired):
        # case C
        i = np.array([2, 8])
        if not ssca:
            # shared spectrum channel access, as described in [15, TS 37.213]s
            if paired:
                if f <= 3e9:
                    n = np.array([0, 1])
                else:
                    n = np.array([0, 1, 2, 3])
            else:
                if f <= 1.88e9:
                    n = np.array([0, 1])
                else:
                    n = np.array([0, 1, 2, 3])
        else:
            n = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        n *= 14
    elif scs == 120e3:
        # case D
        if f >= 6e9:
            i = np.array([4, 8, 16, 20])
            n = np.array([0, 1, 2, 3, 5, 6, 7, 8, 10,
                         11, 12, 13, 15, 16, 17, 18])
            n *= 28
    elif scs == 240e3:
        # case E
        if f >= 6e9:
            i = np.array([8, 12, 16, 20, 32, 36, 40, 44])
            n = np.array([0, 1, 2, 3, 5, 6, 7, 8])
            n *= 56
    can_idxs = np.array([[a + b for a in i] for b in n], dtype=int).flatten()
    if can_idxs is None:
        can_idxs = np.array([], dtype=int)
    return can_idxs


def get_cp_length(mu, l=0,  extended_cp=False):
    kappa = 1  # 64
    if extended_cp:
        return 512 * kappa * 2**(-1 * mu)
    else:
        if l == 0 or l == 7 * 2**mu:
            return 144 * kappa * 2**(-1 * mu) + 16 * kappa
        else:
            return 144 * kappa * 2**(-1 * mu)
