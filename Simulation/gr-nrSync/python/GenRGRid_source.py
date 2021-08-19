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

class GenRGRid_source(gr.sync_block):
    """
    docstring for block GenRGRid_source
    """
    def __init__(self, N_RB, N_ID1, N_ID2, k_ssb, mu, f, shared_spectr, paired_spectr):
        out_len = len(nrSSB.get_sync_resource_grid(
            N_RB, 
            N_ID1, 
            N_ID2, 
            k_ssb, 
            mu, 
            f, 
            shared_spectr, 
            paired_spectr))
        gr.sync_block.__init__(self,
            name="GenRGRid_source",
            in_sig=None,
            out_sig=[np.complex64])
        
        self.N_RB = N_RB
        self.N_ID1 = N_ID1
        self.N_ID2 = N_ID2
        self.k_ssb = k_ssb
        self.mu = mu
        self.f = f
        self.shared_spectr = shared_spectr
        self.paired_spectr = paired_spectr


    def work(self, input_items, output_items):
        out = output_items[0]
        # <+signal processing here+>
        rgrid = nrSSB.get_sync_resource_grid(
            self.N_RB, 
            self.N_ID1, 
            self.N_ID2, 
            self.k_ssb, 
            self.mu, 
            self.f, 
            self.shared_spectr, 
            self.paired_spectr).flatten(order='F')
        out[:] += rgrid
        return len(output_items[0])