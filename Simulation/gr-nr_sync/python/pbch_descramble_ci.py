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

