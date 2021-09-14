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

class decode_sss_ci(gr.sync_block):
    """
    docstring for block decode_sss_ci
    """
    def __init__(self, N_ID2):
        gr.sync_block.__init__(self,
            name="decode_sss_ci",
            in_sig=[(numpy.complex64,127)],
            out_sig=[numpy.int32])
        self.nid2 = N_ID2

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        out[:] = int(nrSyncDecoder.decode_sss(numpy.array(in0[:127],dtype=complex), self.nid2))
        return len(output_items[0])

