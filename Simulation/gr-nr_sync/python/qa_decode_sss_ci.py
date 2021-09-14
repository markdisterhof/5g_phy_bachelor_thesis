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
from decode_sss_ci import decode_sss_ci
import numpy
from nr_phy_sync import nrSyncSignals
class qa_decode_sss_ci(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_t(self):
        # set up fg
        nid2 = 2
        nid1 = 333
        sss_data = numpy.array(nrSyncSignals.sss(nid1, nid2),dtype=numpy.complex64)
        src = blocks.vector_source_c(sss_data,False,127)
        dec = decode_sss_ci(nid2)
        dst = blocks.vector_sink_i(1)
        
        self.tb.connect(src,dec,dst)
        self.tb.run()
        # check data
        numpy.testing.assert_equal(dst.data()[0], nid1)


if __name__ == '__main__':
    gr_unittest.run(qa_decode_sss_ci)
