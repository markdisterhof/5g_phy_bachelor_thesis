#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Mark Disterhof.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr

class pbch_descramble_ci(gr.sync_block):
    """
    docstring for block pbch_descramble_ci
    """
    def __init__(self, L__max):
        gr.sync_block.__init__(self,
            name="pbch_descramble_ci",
            in_sig=[(numpy.complex64,432),(numpy.int32),(numpy.int32)],
            out_sig=[(numpy.int32,864)])
        self.L__max = L__max


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        out[:] = nrSyncDecoder.decode_pbch(
            in0[0],
            self.L__max,
            in0[1],
            in0[2]
        )
        return len(output_items[0])