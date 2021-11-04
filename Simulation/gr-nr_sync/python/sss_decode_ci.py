#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Mark Disterhof.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr
from nrphypy import decode


class sss_decode_ci(gr.sync_block):
    """
    docstring for block sss_decode_ci
    """

    def __init__(self):
        gr.sync_block.__init__(self,
                               name="sss_decode_ci",
                               in_sig=[(numpy.int32, (1,)),
                                       (numpy.complex64, 127)],
                               out_sig=[(numpy.int32, (1,))])

    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        out0 = output_items[0]
        
        for i in range(len(in0)):
            # <+signal processing here+>
            out0[i] = int(decode.decode_sss(
                numpy.array(in1[i], dtype=complex), in0[0][0]))
        return len(out0)
