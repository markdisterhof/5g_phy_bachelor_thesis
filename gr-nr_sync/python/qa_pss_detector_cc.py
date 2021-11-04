#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Mark Disterhof.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, gr_unittest
# from gnuradio import blocks
from pss_detector_cc import pss_detector_cc
import numpy
from nrphypy import ssb

class qa_pss_detector_cc(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_instance(self):
        instance = pss_detector_cc(20,8,80.)

    def test_001_descriptive_test_name(self):
        nrb = 30
        lmax = 8
        nid1 = 10
        nid2 = 2
        kssb = 10
        pbch_data = numpy.random.randint(2, size=864)
        grid = ssb.ssb(nid1, nid2, lmax, 0, pbch_data)
        src_data = ssb.map_ssb(numpy.zeros((nrb*12,6),dtype=numpy.complex64), grid, kssb, 1).flatten(order='F')
        # set up fg
        flat_src = blocks.vector_source_c(src_data, False)
        src = blocks.stream_to_vector(8, nrb*12)
        instance = pss_detector_cc(nrb,lmax,80.)
        nid2_sink = blocks.vector_sink_i()
        ssb_sink = blocks.vector_sink_c(240)
        issb_sink = blocks.vector_sink_i()

        self.tb.connect(flat_src,src)
        self.tb.connect(src,instance)
        self.tb.connect((instance,0),nid2_sink)
        self.tb.connect((instance,1),ssb_sink)
        self.tb.connect((instance,2),issb_sink)
        
        self.tb.run()
        # check data
        #self.assertEqual(nid2, nid2_sink.data())
        #self.assertEqual(0, issb_sink.data())
        print(ssb_sink.data())
        self.assertComplexTuplesAlmostEqual(grid.flatten(order='F'), ssb_sink.data())



if __name__ == '__main__':
    gr_unittest.run(qa_pss_detector_cc)
