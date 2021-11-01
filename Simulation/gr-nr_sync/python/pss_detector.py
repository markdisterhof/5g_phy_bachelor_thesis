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


class pss_detector(gr.basic_block):
    """
    docstring for block pss_detector
    """

    def __init__(self, N_RB, L__max, threshold):
        gr.basic_block.__init__(self,
                                name="pss_detector",
                                in_sig=[(numpy.complex64, N_RB*12)],
                                # nid2, ssb, i_ssb
                                out_sig=[(numpy.int32, (1,)), (numpy.complex64, 240*4), (numpy.int32, (1,))])
        self.N_RB = N_RB
        self.L__max = L__max
        self.threshold = threshold

        self.nid2 = -1
        self.i_ssb = -1
        self.k_ssb = -1
        self.memory = numpy.zeros((240,4),dtype=numpy.complex64)
        self.memory_idx = -1# ssb consists of 4 ofdm syms in time, memorize idx of 

    def forecast(self, noutput_items, ninputs):
        ninput_items_required = [0]*ninputs
        
        # setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items
        return ninput_items_required

    def general_work(self, input_items, output_items):

        samples = input_items[0]
        n_items_produced = 0

        for sample in samples:
            NID_2, k_ssb, max_correlation = nrSyncDecoder.pss_correlate(sample)


            if max_correlation >= self.threshold:  # case corr peak, output next four ofdm symbols
                if not self.memory_idx == -1:  # case prior detected pss was not actually the one with best corr
                    self.i_ssb -= 1

                self.memory_idx = 3
                self.i_ssb += 1
                self.i_ssb %= self.L__max
                
                self.nid2 = NID_2
                
                self.k_ssb = k_ssb

            self.consume_each(1)
            if self.memory_idx > -1:  # write in0 if currently on ssb symbols
                
                
                symbol = sample[self.k_ssb:self.k_ssb+240]
                self.memory[:,3-self.memory_idx] = symbol
                self.memory_idx -= 1
                if self.memory_idx == -1:
                    print('k_ssb, nid2, i_ssb\n',self.k_ssb, self.nid2, self.i_ssb)
                    output_items[2][0] = self.i_ssb
                    output_items[0][0] = self.nid2
                    output_items[1][:] = self.memory.flatten(order='F')
                
                n_items_produced += 1
                return 1

        #consume(0, len(input_items[0]))
        #print('n_items_produced: ', n_items_produced)
        return 0#n_items_produced
