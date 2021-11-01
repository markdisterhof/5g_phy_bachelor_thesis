#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Mark Disterhof.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr


class rgrid_c(gr.sync_block):
    """
    docstring for block rgrid_c
    """

    def __init__(self, N_RB, N_ID1, N_ID2, k_ssb, mu, f, pbch_data, shared_spectr, paired_spectr):
        gr.sync_block.__init__(self,
                               name="rgrid_c",
                               in_sig=None,
                               out_sig=[(np.complex64, N_RB*12)])
        self.resource_grid = np.array(nrSSB.get_sync_resource_grid(
            N_RB, N_ID1, N_ID2, k_ssb, mu, f, shared_spectr, paired_spectr), dtype=np.complex64)
        self.idx = 0

    def work(self, input_items, output_items):
        out = output_items[0]
        # <+signal processing here+>
        out[:] = self.resource_grid[:,self.idx]
        self.idx = (self.idx + 1) % len(self.resource_grid[0])
        # 
        return len(output_items[0])
