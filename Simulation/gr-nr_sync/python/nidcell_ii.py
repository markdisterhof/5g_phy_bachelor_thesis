#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Mark Disterhof.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr

class nidcell_ii(gr.sync_block):
    """
    docstring for block nidcell_ii
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="nidcell_ii",
            in_sig=[(numpy.int32, (1,)),(numpy.int32, (1,))],
            out_sig=[(numpy.int32, (1,))])


    def work(self, input_items, output_items):
        in0 = input_items[0][0]
        in1 = input_items[1][0]
        out = output_items[0]
        # <+signal processing here+>
        #3 * N_ID1 + N_ID2
        out[0] = in0 +3* in1
        print(out[0])
        return len(output_items[0])