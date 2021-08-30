#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 gr-nrSync author.
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


import numpy as np
from gnuradio import gr
from nr_phy_sync import nrSSB

class GenRGRid_c(gr.sync_block):
    """
    docstring for block GenRGRid_c
    """
    def __init__(self, N_RB, N_ID1, N_ID2, k_ssb, mu, f, shared_spectr, paired_spectr):
        self.resource_grid = np.array(nrSSB.get_sync_resource_grid(N_RB, N_ID1, N_ID2, k_ssb, mu, f, shared_spectr, paired_spectr), dtype= np.complex64)
        self.idx = 0
        gr.sync_block.__init__(self,
            name="GenRGRid_c",
            in_sig=None,
            out_sig=[(np.complex64, N_RB*12)])


    def work(self, input_items, output_items):
        out = output_items[0]
        # <+signal processing here+>
        out[:] += self.resource_grid[:,self.idx]
        self.idx = (self.idx + 1) % len(self.resource_grid[0])
        return len(output_items[0])