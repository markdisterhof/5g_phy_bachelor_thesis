#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Mark Disterhof.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr
from nr_phy_sync import nrSSB


class rgrid_c(gr.sync_block):
    """
    docstring for block rgrid_c
    """

    def __init__(self, n_carr, N_ID1, N_ID2, k_ssb, mu, f, pbch_data, shared_spectr, paired_spectr):
        gr.sync_block.__init__(self,
                               name="rgrid_c",
                               in_sig=None,
                               out_sig=[(numpy.complex64, (1,))])
                               
        self.resource_grid = nrSSB.grid(n_carr, N_ID1, N_ID2, k_ssb, mu, f, shared_spectr, paired_spectr, pbch_data).flatten(order='F')#numpy.array(range(n_carr),dtype=complex)
        numpy.save('/home/mark/ssb.npy', self.resource_grid)
        self.idx = 0
        #self.set_output_multiple(n_carr)

    def work(self, input_items, output_items):
        out = output_items[0]
        n_items = len(out)
        output_items[0][:] = numpy.take(self.resource_grid,
                         range(self.idx, self.idx+n_items),
                         mode='wrap').reshape((n_items, 1))
        self.idx += n_items
        self.idx %= len(self.resource_grid)
        return n_items  # len(out)
