#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 gr-nrSync author.
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
from GenRGRid_source import GenRGRid_source
import numpy as np

class qa_GenRGRid_source(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_t(self):
        tb = self.tb
        # set up fg
        tb.run()
        # check data
        b = np.load('../../syncrgrid_20_0_1_0_1_0_T_F.npy').flatten(order='F')
        src1 = GenRGRid_source(20,0,1,0,1,0,True,False)
        dst0 = blocks.stream_to_vector(len(b),len(b))
        dst1 = blocks.vector_sink_c(len(b))
        tb.connect(src1, dst0)
        tb.connect(dst0, dst1)
        tb.run()
        a = dst1.data()
        
        np.testing.assert_array_equal(a,b)

if __name__ == '__main__':
    gr_unittest.run(qa_GenRGRid_source)
