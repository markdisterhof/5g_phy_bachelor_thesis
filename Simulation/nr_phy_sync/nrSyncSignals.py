import numpy as np

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
    x_1 = np.array([1]+[0]*(n + len(c) + N_c-1))
    x_2 = np.zeros((n + len(c) + N_c))
    x_2_c = np.flip([int(x) for x in bin(c_init)[2:]])
    x_2[:len(x_2_c)] = x_2_c
        
    for n_i in range(n + N_c - 31):
        x_1[n_i+31] = (x_1[n_i+3] + x_1[n_i]) % 2 
        x_2[n_i+31] = (x_2[n_i+3] + x_2[n_i+2] + x_2[n_i+1] + x_2[n_i]) % 2

    for n_i in range(n):
        c[n_i] = (x_1[n_i + N_c] + x_2[n_i + N_c]) % 2
    return c


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


def pbch(b, L__max, N_ID_Cell, i_SSB):
    """Generate physical broadcast channel sequence
    
    TS 38.211 V16.2.0 (2020-07)

    7.3.3 Physical broadcast channel
    
    Args:
        b ([int]): PBCH payload bits
        L__max (int): Maximum number of candidate SS/PBCH blocks in a half frame
        N_ID_Cell (int): Cell identity ID
        i_SSB (int): Candidate SS/PBCH block index

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
        v = i_SSB % 2**2
    else:
        v = i_SSB % 2**3

    c = prsg((1+v) * M_bit, N_ID_Cell)

    b_ = [(b[i] + c[i + v * M_bit]) % 2 for i in range(M_bit)]

    d_PBCH = sym_qpsk(b_)
    return d_PBCH

def sym_qpsk(b):
    """Modulate a list of bits with QPSK as per

    TS 38.211 V16.2.0 (2020-07) 5.1.3

    Args:
        b ([int]): List of bits to modulate
    """    

    return np.array(
        [(1-2*b[2*i]+1j*(1-2*b[2*i+1]))/np.sqrt(2) for i in range(len(b)//2)],
        dtype=complex)

def inv_sym_qpsk(c):
    c = np.array(c,dtype=complex).flatten() #weird python type error in gr
    b_ = np.array(
        [[int(np.round(np.real(i)*np.sqrt(2))),int(np.round(np.imag(i)*np.sqrt(2)))] for i in c]
        ,dtype=int
        ).flatten()
    return np.array([(1-b_i)//2 for b_i in b_], dtype=int)