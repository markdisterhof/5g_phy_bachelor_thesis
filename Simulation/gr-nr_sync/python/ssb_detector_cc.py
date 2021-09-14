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
from nr_phy_sync import nrSSB

class ssb_detector_cc(gr.sync_block):
    """
    docstring for block ssb_detector_cc
    """
    def __init__(self,n_rb: int, mu: int, f: int, shared_spectr: bool, paired_spectr: bool):
        
        N_SC, N_SYMB_FRAME = nrSSB.get_rgrid_dimensions(mu, n_rb)
        self.FRAME_SIZE = int(N_SC * N_SYMB_FRAME)
        self.idxs = nrSSB.get_ssb_idxs(
            nrSSB.get_ssb_candidate_idx(
                mu, f, shared_spectr, paired_spectr
            ), mu, shared_spectr
        )
        self.i_ssb = 0
        self.ssb = numpy.zeros((len(self.idxs),240,4),dtype=numpy.complex64)
        
        ssb_sym_ratio = float(N_SYMB_FRAME) / float(len(self.idxs))

        gr.sync_block.__init__(self,
            name="ssb_detector_cc",
            in_sig=[(numpy.complex64,n_rb * N_SYMB_FRAME)],
            out_sig=[(numpy.complex64,4*240),(numpy.uint8)])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        out[:] = in0
        return len(output_items[0])
