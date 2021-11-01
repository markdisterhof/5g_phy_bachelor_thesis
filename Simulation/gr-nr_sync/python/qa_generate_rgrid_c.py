#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Mark Disterhof 2021.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from generate_rgrid_c import generate_rgrid_c
import numpy as np
from nr_phy_sync import nrSSB

class qa_generate_rgrid_c(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_t(self):
        test_data = nrSSB.get_sync_resource_grid(20,0,1,0,1,0,True,False)
        # set up fg
        src = generate_rgrid_c(N_RB=20,N_ID1=0,N_ID2=1,k_ssb=0,mu=1,f=0,pbch_data=[0],shared_spectr=True,paired_spectr=False)
        head = blocks.head(nitems= len(test_data.T), sizeof_stream_item= 20*12*8)
        dst = blocks.vector_sink_c(vlen=20*12)
        #
        self.tb.connect(src,head,dst)
        self.tb.run()
        # check data
        np.save('test_data', dst.data())
        np.testing.assert_array_almost_equal(dst.data(),test_data)

if __name__ == '__main__':
    gr_unittest.run(qa_generate_rgrid_c)
