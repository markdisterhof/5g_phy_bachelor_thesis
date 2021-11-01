#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Mark Disterhof.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr
from nr_phy_sync import nrSyncDecoder


class pbch_descramble_ci(gr.sync_block):
    """
    docstring for block pbch_descramble_ci
    """

    def __init__(self, L__max):
        gr.sync_block.__init__(self,
                               name="pbch_descramble_ci",
                               in_sig=[
                                   (numpy.int32),
                                   (numpy.complex64, 432),
                                   (numpy.int32)],
                               out_sig=[(numpy.int32, 864)])
        self.L__max = L__max

    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        in2 = input_items[2]
        out0 = output_items[0]

        # <+signal processing here+>
        for i in range(len(in1)):
            out0[i] = nrSyncDecoder.decode_pbch(
                in1[i],
                self.L__max,
                in0[i],
                in2[i]
            )
        return len(out0)
