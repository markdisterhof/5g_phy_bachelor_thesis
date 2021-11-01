#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Mark Disterhof.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, gr_unittest
# from gnuradio import blocks
from sss_decode_ci import sss_decode_ci

class qa_sss_decode_ci(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_instance(self):
        # FIXME: Test will fail until you pass sensible arguments to the constructor
        instance = sss_decode_ci()

    def run_dec(self, nid1,nid2):
        print('testing nid1,nid2', nid1,nid2)
        self.setUp()
        sss_data = numpy.array(nrSyncSignals.sss(nid1, nid2),dtype=numpy.complex64)
        src_0 = blocks.vector_source_i([nid2],False)
        src_1 = blocks.vector_source_c(sss_data,False,127)
        dec = sss_decode_ci()
        dst = blocks.vector_sink_i(1)
        
        self.tb.connect(src_0,(dec,0))
        self.tb.connect(src_1,(dec,1))
        self.tb.connect(dec, dst)
        self.tb.run()
        # check data
        print(dst.data(), [nid1])
        self.assertEqual(dst.data(), [nid1])
        self.tearDown()

    def test_001_t(self):
        # set up fg
        confs = [(nid1,nid2) for nid1 in range(16,23) for nid2 in range(3)]
        for conf in confs:
            self.run_dec(*conf)


if __name__ == '__main__':
    gr_unittest.run(qa_sss_decode_ci)
