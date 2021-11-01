#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Mark Disterhof.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from unmap_ssb_cc import unmap_ssb_cc
import numpy
from nr_phy_sync import nrSSB

class qa_unmap_ssb_cc(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_instance(self):
        # FIXME: Test will fail until you pass sensible arguments to the constructor
        instance = unmap_ssb_cc(1)

    def test_001_descriptive_test_name(self):
        ssb_dim = {
            'l': 4,
            'k': 240,
            'nu':3
        }
        pss_data = numpy.ones(127)
        sss_data = numpy.ones(127)*2
        pbch_data = numpy.ones(432)*3
        dmrs_data = numpy.ones(144)*4
        ssb = numpy.zeros((240, 4), dtype=complex) + \
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
        
        numpy.testing.assert_equal(nrSSB.unmap_sss(ssb), snk0.data())
        numpy.testing.assert_equal(nrSSB.unmap_pbch(ssb,ssb_dim)[0], snk1.data())
        numpy.testing.assert_equal(nrSSB.unmap_pbch(ssb,ssb_dim)[1], snk3.data())
        numpy.testing.assert_equal([0], snk2.data())


if __name__ == '__main__':
    gr_unittest.run(qa_unmap_ssb_cc)
