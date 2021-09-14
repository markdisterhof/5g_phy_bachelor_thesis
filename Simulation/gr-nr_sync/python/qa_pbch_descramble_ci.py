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
from pbch_descramble_ci import pbch_descramble_ci
import numpy
from nr_phy_sync import nrSyncDecoder, nrSyncSignals

class qa_pbch_descramble_ci(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_t(self):
        b = numpy.random.randint(2, size=864)
        L__max, N_ID_Cell, i_SSB = (5,325,2)
        pbch = nrSyncSignals.pbch(b,L__max, N_ID_Cell, i_SSB)
        # set up fg
        src = blocks.vector_source_c(pbch,False,len(pbch))
        dec = pbch_descramble_ci(L__max, N_ID_Cell, i_SSB)
        dst = blocks.vector_sink_i(len(b))
        
        self.tb.connect(src,dec,dst)
        self.tb.run()
        # check data
        numpy.testing.assert_equal(b, dst.data())

if __name__ == '__main__':
    gr_unittest.run(qa_pbch_descramble_ci)
