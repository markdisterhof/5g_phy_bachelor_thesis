import numpy as np
from pyphysim.modulators import QPSK # todo

def prsg(n, c_init):
    """Compute c as per
    
    TS 38.211 16.2.0 (2020-07)
    
    5.2.1 Pseudo-random sequence generation

    Args:
        n (int): sequence length (= M_PN)
        c_init (initializer): initializer

    Returns:
        ndarray: pseudo-random sequence of length n
    """
    c = np.zeros(n)
    N_c = 1600
    x_1 = np.array([1])
    x_1.resize(n + len(c) + N_c)
    x_2 = np.array(np.flip([int(x) for x in bin(c_init)[2:]]))
    x_2.resize((n + len(c) + N_c))
        
    for n_i in range(n + N_c - 31):
        x_1[n_i+31] = (x_1[n_i+3] + x_1[n_i]) % 2 
        x_2[n_i+31] = (x_2[n_i+3] + x_2[n_i+2] + x_2[n_i+1] + x_2[n_i]) % 2

    for n_i in range(n):
        c[n_i] = (x_1[n_i + N_c] + x_2[n_i + N_c]) % 2
    return c


def g_CRC24C(a):
    """CRC calculation 
    
    TS 38.212 16.2.0 (2020-07) 

    5.1 CRC calculation

    Args:
        a ([int]): input bits
    """    
                    #24,23,   21, 20,      17,   15,  13, 12,   8,          4,    2, 1, 0   
    gen_polynomial = [1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1]
    p = np.zeros(len(gen_polynomial), dtype = int)
    a_ = np.concatenate([a, p])
    for i in range(len(a)):
        if a_[i] == 1:
            a_[i:i + len(p)] = a_[i:i + len(p)] ^ gen_polynomial
    p[:] = a_[len(a):]
    return p

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
    scs = 2**mu *15e3

    if scs == 15e3:
        # case A
        i = np.array([2,8])
        if ssca:
            # shared spectrum channel access, as described in [15, TS 37.213]s
            n = np.array([0,1,2,3,4])
        elif f <= 3e9:
            n = np.array([0,1])
        else:
            n = np.array([0,1,2,3])
        n *= 14

    elif scs == 30e3 and not (ssca or paired):
        # case B
        i = np.array([4,8,16,20])
        if f <= 3e9:
            n = np.array([0])
        else:
            n = np.array([0,1])
        n *= 28

    elif scs == 30e3 and (ssca or paired):
        # case C
        i = np.array([2,8])
        if not ssca:
            # shared spectrum channel access, as described in [15, TS 37.213]s
            if paired:
                if f <= 3e9:
                    n = np.array([0,1])
                else:
                    n = np.array([0,1,2,3])
            else:
                if f <= 1.88e9:
                    n = np.array([0,1])
                else:
                    n = np.array([0,1,2,3])
        else:
            n = np.array([0,1,2,3,4,5,6,7,8,9])
        n *= 14
    elif scs == 120e3:
        # case D
        if f >= 6e9:
            i = np.array([4,8,16,20])
            n = np.array([0,1,2,3,5,6,7,8,10,11,12,13,15,16,17,18])
            n *= 28
    elif scs == 240e3:
        # case E
        if f >= 6e9:
            i = np.array([8,12,16,20,32,36,40,44])
            n = np.array([0,1,2,3,5,6,7,8])
            n *= 56
    
    return np.array([[a + b for a in i] for b in n], dtype=int).flatten()


def pss(N_ID2):
    """Generate primary synchronization signal as per

    TS 38 211 V16.2.0 (2020-07)

    7.4.2.2 Primary synchronization signal

    Args:
        N_ID2 (int):  cell ID sector

    Returns:
        [int]: primary synchronization signal sequence (127 bits)
    """
    x = [1, 0, 0, 0, 0, 0, 0]
    d_pss = []
    n = 127

    for i in range(n-len(x)):
        x.append(
            (x[i+4] + x[i]) % 2)
    
    for n_i in range(n):
        d_pss.append( 
            1 - 2 * x[(n_i + 43 * N_ID2) % 127])
        
    return d_pss

def sss(N_ID1, N_ID2):
    """Generate secondary synchronization signal as per

    TS 138 211 V16.2.0 (2020-07)

    7.4.2.3 Secondary synchronization signal

    Args:
        N_ID1 (int): cell ID group
        N_ID2 (int): cell ID sector

    Returns:
        [int]: secondary synchronization signal sequence (127 bits)
    """    

    x_0 = [0, 0, 0, 0, 0, 0, 1]
    x_1 = [0, 0, 0, 0, 0, 0, 1]
    d_sss = []
    m_0 = 15*(N_ID1//112) + 5 * N_ID2
    m_1 = N_ID1 % 112
    n = 127

    for i in range(n-len(x_0)):
        x_0.append(
            (x_0[i+4] + 4 * x_0[i] ) % 2)
        x_1.append(
            (x_1[i+1] + x_1[i]) % 2)
    
    for n_i in range(n):
        d_sss.append(
            (1 - 2 * x_0[(n_i + m_0) % 127]) *
            (1 - 2 * x_1[(n_i + m_1) % 127]))
        
    return d_sss


# 7.4.1.4.1 
def dmrs(i_ssb, N_ID_Cell, L__max, n_hf = 0):
    """Generate Demodulation reference signals for PBCH as per 

    TS 38.211 V16.2.0 (2020-07)

    7.4.1.4 Demodulation reference signals for PBCH 

    Args:
        i_ssb (int): Candidate SS/PBCH block index
        N_ID_Cell (int): Cell identity ID
        L__max (int): Maximum number of candidate SS/PBCH blocks in a half frame
        n_hf (int, optional): Number of the half-frame in which the PBCH is transmitted in a frame n_hf=0: first half-frame,n_hf=1: second half-frame . Defaults to 0.

    Returns:
        [complex]: Demodulation reference signals for PBCH
    """        
    M = 144
    i_ssb_= None

    if L__max == 4:
        i_ssb_ = i_ssb % 4 + 4 * n_hf
    elif L__max > 4:
        i_ssb_ = i_ssb % 8
    
    c_init = int(2**11 * (i_ssb_ + 1) * ((N_ID_Cell // 4 )+1) +
        2**6 * (i_ssb_ +1) +
        (N_ID_Cell % 4))

    c = prsg(2 * M + 1, c_init )

    r = np.zeros(M, dtype = complex)
    for m in range(M):
        r[m] = (1 - 2 * c[2 * m] + (1 - 2 * c[2 * m + 1]) * 1j)/np.sqrt(2) # compute complex symbols
    return r


def pbch(b, L__max, N_ID_Cell, ssb_idx):
    """Generate physical broadcast channel sequence
    
    TS 38.211 V16.2.0 (2020-07)

    7.3.3 Physical broadcast channel
    
    Args:
        b ([int]): PBCH payload bits
        L__max (int): Maximum number of candidate SS/PBCH blocks in a half frame
        N_ID_Cell (int): Cell identity ID
        ssb_idx (int): Candidate SS/PBCH block index

    Raises:
        ValueError: PBCH payload data must be 864 symbols

    Returns:
        [complex]: modulated pbch sequence as per 
    """

    M_bit = len(b)
    if not M_bit == 864:
        raise ValueError('PBCH payload data must be 864 symbols')

    v = None
    if L__max == 4:
        v = ssb_idx % 4
    else:
        v = ssb_idx % 8

    c = prsg((1+v) * M_bit, N_ID_Cell)

    b_ = [(b[i] + c[i + v * M_bit]) % 2 for i in range(M_bit)]

    d_PBCH = bit_qpsk(b_)
    return d_PBCH


def map_pss(data, ssb_dim, beta = 1.):
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
    mask = np.zeros((ssb_dim['k'], ssb_dim['l']), dtype= complex)
    data = np.array(data) * beta
    mask[56:183, 0] = data
    return mask

def map_sss(data, ssb_dim, beta = 1.):
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
    mask = np.zeros((ssb_dim['k'], ssb_dim['l']), dtype= complex)
    data = np.array(data) * beta
    mask[56:183, 2] = data
    return mask

def map_pbch(data_pbch, data_dmrs, ssb_dim, beta_pbch = 1., beta_dmrs = 1.):
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
        raise ValueError("pbch is always 432 symbols, dmrs is always 144 symbols")
    i_dmrs, i_pbch = 0, 0

    data_pbch = np.array(data_pbch) * beta_pbch
    data_dmrs = np.array(data_dmrs) * beta_dmrs

    mask = np.zeros((ssb_dim['k'], ssb_dim['l']),dtype=complex)
    if not any(np.iscomplex(np.concatenate((data_pbch, data_dmrs)))):
        mask = np.zeros((ssb_dim['k'], ssb_dim['l']), dtype=int)
    for l in range(1,4):
        k_range = range(240)
        if l == 2 :
            k_range = np.concatenate((range(48),range(192,240)))
        for k in k_range:
            if k % 4 == ssb_dim['nu']:
                mask[k, l] = data_dmrs[i_dmrs]
                i_dmrs += 1
            else:
                mask[k, l] = data_pbch[i_pbch]
                i_pbch += 1
    return mask

def ssb(ssb_dim, N_ID1, N_ID2, L__max, ssb_idx):
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

    ssb = np.zeros((ssb_dim['k'],ssb_dim['l']), dtype = complex) # one ssb

    # pss mapping
    data_pss = pss(N_ID2 = N_ID2)

    ssb += map_pss(data_pss, ssb_dim)


    # sss mapping
    data_sss =  sss(
        N_ID1 = N_ID1,
        N_ID2 = N_ID2)

    ssb += map_sss(data_sss, ssb_dim)


    #pbch and dmrs mapping
    data_pbch = pbch(
        np.random.randint(2, size=864),
        L__max,
        N_ID_Cell,
        ssb_idx)
    
    data_dmrs = dmrs(ssb_idx, N_ID_Cell, L__max, 0)

    ssb += map_pbch(data_pbch, data_dmrs, ssb_dim)
    return ssb



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
    nid2_candidates = np.array([pss(N_ID2 = n_id2) for n_id2 in range(3)])
    
    corr = np.zeros((3, received_data.shape[0], received_data.shape[1]), dtype=complex)
    
    for (i,pss_i) in enumerate(nid2_candidates):
        rgrid_mask = np.zeros(rec_pss_sym.shape, dtype=complex)
        rgrid_mask[:ssb_dim['k'], :ssb_dim['l']] += map_pss(pss_i, ssb_dim)
        
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
    sss_candidates = np.array([sss(
        N_ID1 = nid1,
        N_ID2 = nid2) for nid1 in range(336)])
    
    corr = np.zeros(len(sss_candidates),dtype=complex)
    
    for i,sss_i in enumerate(sss_candidates):
        corr[i] = np.multiply(sss_i, sss_data).sum()
    
    return max(np.unravel_index(np.argmax(corr, axis=None), corr.shape))



def unmap_pss(received_data, ssb_dim):
    """Unmap PSS from given resource grid

    Args:
        received_data ([complex, complex]): 2D resource grid
        ssb_dim (struct): SSB dimensions and nu 

    Returns:
        [complex]: PSS data
    """
    ssb_mask = np.zeros((ssb_dim['k'], ssb_dim['l']), dtype = int)
    ssb_mask += map_pss(np.ones(127), ssb_dim)
    mask_rgrid = np.zeros(received_data.shape)
    print(mask_rgrid.shape, ssb_mask.shape, ssb_dim)
    mask_rgrid[ssb_dim['k_offset']:ssb_dim['k_offset']+240, ssb_dim['l_offset']:ssb_dim['l_offset']+4] = ssb_mask
    return received_data[
        np.nonzero(
            np.multiply(mask_rgrid, received_data))]

def unmap_sss(received_data, ssb_dim):
    """Unmap SSS from given resource grid

    Args:
        received_data ([complex, complex]): 2D resource grid
        ssb_dim (struct): SSB dimensions and nu 

    Returns:
        [complex]: SSS data
    """
    ssb_mask = np.zeros((ssb_dim['k'], ssb_dim['l']), dtype=complex)
    ssb_mask += map_sss(np.ones(127, dtype=complex), ssb_dim)
    mask_rgrid = np.zeros(received_data.shape, dtype=complex)
    mask_rgrid[ssb_dim['k_offset']:ssb_dim['k_offset']+240, ssb_dim['l_offset']:ssb_dim['l_offset']+4] = ssb_mask
    return received_data[
        np.nonzero(
            np.multiply(mask_rgrid, received_data))]

def unmap_pbch(received_data, ssb_dim):
    """Unmap PBCH and DM-RS from given resource grid

    Args:
        received_data ([complex, complex]): 2D resource grid
        ssb_dim (struct): SSB dimensions and nu 

    Returns:
        tuple: PBCH and DM-RS data
    """
    ssb_mask_pbch = np.zeros((ssb_dim['k'], ssb_dim['l']), dtype = int)
    ssb_mask_dmrs = np.zeros((ssb_dim['k'], ssb_dim['l']), dtype = int)

    ssb_mask_pbch += map_pbch(np.ones(432), np.zeros(144), ssb_dim)
    ssb_mask_dmrs += map_pbch(np.zeros(432), np.ones(144), ssb_dim)

    mask_rgrid_pbch = np.zeros(received_data.shape)
    mask_rgrid_dmrs = np.zeros(received_data.shape)

    mask_rgrid_pbch[ssb_dim['k_offset']:ssb_dim['k_offset']+240, ssb_dim['l_offset']:ssb_dim['l_offset']+4] = ssb_mask_pbch
    mask_rgrid_dmrs[ssb_dim['k_offset']:ssb_dim['k_offset']+240, ssb_dim['l_offset']:ssb_dim['l_offset']+4] = ssb_mask_dmrs

    data_pbch = received_data.flatten(order='F')[np.nonzero(np.multiply(mask_rgrid_pbch, received_data).flatten(order='F'))]
    data_dmrs = received_data.flatten(order='F')[np.nonzero(np.multiply(mask_rgrid_dmrs, received_data).flatten(order='F'))]

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
    res_grid[k_offs:len(ssb)+k_offs, l_offs:len(ssb[0,:])+l_offs] = ssb
    return res_grid

def calc_ksbb(mib, offsetToPointA ):
    pass

def bit_qpsk(b):
    """Modulate a list of bits with QPSK as per

    TS 38.211 V16.2.0 (2020-07) 5.1.3

    Args:
        b ([int]): List of bits to modulate

    Raises:
        ValueError: len(b) must be an even number

    Returns:
        [type]: [description]
    """    
    n = 2
    if len(b) % 2:
        raise ValueError('len(b) must be an even number')

    v = [2**i for i in range(n)]
    syms = np.array(
        [np.multiply(v, b[i:i+n]).sum() for i in range(0,len(b),n)], 
        dtype=int)
    return QPSK().modulate(syms)

def get_sync_resource_grid(N_RB, N_ID1, N_ID2, k_ssb, mu, f, shared_spectr = False, paired_spectr = False):
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
        'l' : 4,
        'k' : 240,
        'nu' : N_ID_Cell % 4
    }
    N_SC, N_SYMB = get_rgrid_dimensions(mu, N_RB)


    can_idxs = get_ssb_candidate_idx(mu, f, shared_spectr, paired_spectr)
    L__max = len(can_idxs)
    idxs = get_ssb_idxs(can_idxs, mu, shared_spectr)
    res_grid = np.zeros(shape=( N_SC, N_SYMB), dtype=complex)

    for idx in idxs:
        ssb_i = ssb(ssb_dim, N_ID1, N_ID2, L__max, idx)
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

def get_cp_length(mu, l = 0,  extended_cp = False):
    kappa = 1#64
    if extended_cp:
        return 512 * kappa * 2**(-1 * mu)
    else:
        if l == 0 or l == 7 * 2**mu:
            return 144 * kappa * 2**(-1 * mu) + 16 * kappa
        else:
            return 144 * kappa * 2**(-1 * mu)


def get_ssb_idxs(candidate_idxs, mu, shared_spectr):
    if shared_spectr:
        if (len(candidate_idxs)==10 and mu == 0) or (len(candidate_idxs)==20 and mu == 1):
            return candidate_idxs[:8]
    else:
        return candidate_idxs


def get_channel_profile(channel_profile : str, ds_desired=1e-9):

    TDL_A = [
        np.array([-13.4, 0., -2.2, -4., -6., -8.2, -9.9, -10.5, -7.5, -15.9, -6.6, -16.7, -12.4, -15.2, -10.8, -11.3, -12.7, -16.2, -18.3, -18.9, -16.6, -19.9, -29.7]),
        np.array([0., 0.3819, 0.4025, 0.5868, 0.4610, 0.5375, 0.6708, 0.5750, 0.7618, 1.5375, 1.8978, 2.2242, 2.1718, 2.4942, 2.5119, 3.0582, 4.0810, 4.4579, 4.5695, 4.7966, 5.0066, 5.3043, 9.6586]),
        'TDL-A'
    ]

    TDL_B = [
        np.array([0., -2.2, -4., -3.2, -9.8, -1.2, -3.4, -5.2, -7.6, -3, -8.9, -9., -4.8, -5.7, -7.5, -1.9, 7.6, -12.2, -9.8, -11.4, -14.9, -9.2, -11.3 ]),
        np.array([0., 0.1072, 0.2155, 0.2095, 0.2870, 0.2986, 0.3752, 0.5055, 0.3681, 0.3697, 0.57, 0.5283, 1.1021, 1.2765, 1.5474, 1.7842, 2.0169, 2.8294, 3.0219, 3.6187, 4.1067, 4.2790, 4.7834]),
        'TDL-B'
    ]

    TDL_C = [
        np.array([-4.4, -1.2, -3.5, -5.2, -2.5, 0., -2.2, -3.9, -7.4, -7.1, -10.7, -11.1, -5.1, -6.8, -8.7, -13.2, -13.9, -13.9, -15.8, -17.1, -16., -15.7, -21.6, -22.8]),
        np.array([0., 0.2099, 0.2219, 0.2329, 0.2176, 0.6366, 0.6446, 0.6560, 0.6584, 0.7935, 0.8213, 0.9336, 1.2285, 1.3083, 2.1704, 2.7105, 4.2589, 4.6003, 5.4902, 5.6077, 6.3065, 6.6374, 7.0427, 8.6523]),
        'TDL-C'
    ]

    threegpp_channel_profiles = {
        'TDL_A' : TDL_A,
        'TDL_B' : TDL_B,
        'TDL_C' : TDL_C
    }

    ch_pr = threegpp_channel_profiles[channel_profile]
    ch_pr[1] *= ds_desired
    return ch_pr

'''
TODO:
[* cp size]
'''
