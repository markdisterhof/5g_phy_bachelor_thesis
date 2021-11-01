#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Mark Disterhof.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr


class unmap_ssb_cc(gr.sync_block):
    """
    docstring for block unmap_ssb_cc
    """

    def __init__(self, nu):
        gr.sync_block.__init__(self,
                               name="unmap_ssb_cc",
                               in_sig=[(numpy.complex64, 4*240),
                                       (numpy.int32, (1,))],
                               out_sig=[
                                   (numpy.complex64, 127),  # sss
                                   (numpy.complex64, 432),  # pbch
                                   ((numpy.int32, (1,))),  # i_ssb
                                   (numpy.complex64, 144)])  # dmrs
        self.nu = nu

    def work(self, input_items, output_items):
        ssb_dim = {
            'l': 4,
            'k': 240,
            'nu': self.nu
        }

        in0 = input_items

        ssb = numpy.array(in0[0][0], dtype=complex).reshape(
            (240, 4), order='F')

        out = output_items
        # <+signal processing here+>
        sss_data = nrSSB.unmap_sss(ssb)
        pbch_data, dmrs_data = nrSSB.unmap_pbch(ssb, ssb_dim)
        out[0][0] = sss_data
        out[1][0] = pbch_data
        out[2][0] = in0[1][0]
        out[3][0] = dmrs_data
        return 1
