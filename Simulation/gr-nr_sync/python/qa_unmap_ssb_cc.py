#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Mark Disterhof.
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
from unmap_ssb_cc import unmap_ssb_cc
import numpy as np
from nr_phy_sync import nrSSB


class qa_unmap_ssb_cc(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001(self):
        ssb_dim = {
            'l': 4,
            'k': 240,
            'nu':3
        }
        pss_data = np.ones(127, dtype=complex)
        sss_data = np.ones(127, dtype=complex)*2
        pbch_data = np.ones(432, dtype=complex)*3
        dmrs_data = np.ones(144, dtype=complex)*4
        ssb = np.zeros((240, 4), dtype=complex) + \
            nrSSB.map_pss(pss_data, ssb_dim) + \
            nrSSB.map_sss(sss_data, ssb_dim) +\
            nrSSB.map_pbch(pbch_data, dmrs_data, ssb_dim)
        src_data = ssb.flatten(order='F')

        # set up fg
        src = blocks.vector_source_c(src_data,False,240*4)
        src1 = blocks.vector_source_i([0],False)
        inst = unmap_ssb_cc(3)
        snk0 = blocks.vector_sink_c(127)
        snk1 = blocks.vector_sink_c(432)
        snk2 = blocks.vector_sink_i()
        snk3 = blocks.vector_sink_c(144)
        self.tb.connect(src,(inst,0))
        self.tb.connect(src1,(inst,1))
        self.tb.connect((inst,0),snk0)
        self.tb.connect((inst,1),snk1)
        self.tb.connect((inst,2),snk2)
        self.tb.connect((inst,3),snk3)
        self.tb.run()
        # check data
        self.assertComplexAlmostEqual(nrSSB.unmap_sss(ssb), snk0.data())
        self.assertComplexAlmostEqual(nrSSB.unmap_pbch(ssb)[0], snk1.data())
        self.assertComplexAlmostEqual(nrSSB.unmap_pbch(ssb)[1], snk3.data())
        self.assertEqual(0, snk2.data())

if __name__ == '__main__':
    gr_unittest.run(qa_unmap_ssb_cc)
