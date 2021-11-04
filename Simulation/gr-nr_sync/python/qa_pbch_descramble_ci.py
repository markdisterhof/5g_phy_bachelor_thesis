#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Mark Disterhof.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from pbch_descramble_ci import pbch_descramble_ci
import numpy

class qa_pbch_descramble_ci(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_instance(self):
        # FIXME: Test will fail until you pass sensible arguments to the constructor
        instance = pbch_descramble_ci()

    def test_001_descriptive_test_name(self):
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
        self.assertEqual(b, dst.data())
        #numpy.testing.assert_equal(b, dst.data())


if __name__ == '__main__':
    gr_unittest.run(qa_pbch_descramble_ci)
