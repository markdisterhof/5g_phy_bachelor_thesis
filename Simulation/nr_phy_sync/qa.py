import numpy as np
from nr_phy_sync import nrSyncDecoder, nrSSB
#todo make actual tests


for i in range(8):
    data = np.random.randint(2, size=864)
    ssb = nrSSB.ssb(ssb_dim, 0, 0, 8, i, data)
    pbch = nrSSB.unmap_pbch(ssb,ssb_dim)[0]
    dec = nrSyncDecoder.decode_pbch(pbch,8,0,i)
    np.testing.assert_equal(data, dec)



idxs = nrSSB.get_ssb_idxs(nrSSB.get_ssb_candidate_idx(0, 0, True, False),0,True)
pbch_d = np.zeros((len(idxs), 864), dtype=int)
for i_ssb,idx in enumerate(idxs):
    ssb_dim= {'l': 4, 'k': 240, 'nu': 0}
    pbch = nrSSB.unmap_pbch(ssb[:,idx:idx+4],ssb_dim)[0]
    pbch_d[i_ssb,:] = nrSyncDecoder.decode_pbch(pbch,8,0,i_ssb)
dec = pbch_d.flatten()[:len(a)].copy()
#np.testing.assert_equal(dec,a)
dec.resize((35,201))
#plot_grid(dec.reshape(35,201))
plt.imshow(dec.reshape(35,201),interpolation='nearest', aspect='auto')