#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Mark Disterhof.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr
from nr_phy_sync import nrSyncDecoder,nrSSB

class pss_detector_cc(gr.basic_block):
    """
    docstring for block pss_detector_cc
    """
    def __init__(self, n_carr, L__max, threshold):
        gr.basic_block.__init__(self,
            name="pss_detector_cc",
                            in_sig=[(numpy.complex64, n_carr)],
                                # nid2, ssb, i_ssb
                                out_sig=[(numpy.int32, (1,)), (numpy.complex64, 240*4), (numpy.int32, (1,))])

        self.L__max = L__max
        self.threshold = threshold

        self.nid2 = -1
        self.i_ssb = -1
        self.k_ssb = -1
        self.memory = numpy.zeros((240,4),dtype=numpy.complex64)
        self.memory_idx = -1# ssb consists of 4 ofdm syms in time, memorize idx of 
        self.last_sample= -1
        self.no_ssb_counter = 0
        self.reset = 100

    def forecast(self, noutput_items, ninputs):
        ninput_items_required = [0]*ninputs
        
        # setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items
        return ninput_items_required

    def general_work(self, input_items, output_items):
        samples = input_items[0]
        n_items_produced = 0
        
        for i, sample in enumerate(samples):
            if numpy.array_equal(sample,self.last_sample):
                continue
            self.last_sample = sample
            NID_2, k_ssb, max_correlation = nrSyncDecoder.pss_correlate(sample)
            
            if max_correlation >= self.threshold:  # case corr peak, output next four ofdm symbols
                if not self.memory_idx == -1:  # case prior detected pss was not actually the one with best corr
                    self.i_ssb -= 1

                self.memory_idx = 3
                self.i_ssb += 1
                self.i_ssb %= self.L__max
                self.nid2 = NID_2
                
                self.k_ssb = k_ssb

            
            if self.memory_idx > -1:  # write in0 if currently on ssb symbols
                
                symbol = sample[self.k_ssb:self.k_ssb+240]
                self.memory = numpy.roll(self.memory, (0,-1))
                self.memory[:,3] = symbol
                self.memory_idx -= 1

                if self.memory_idx == -1:
                    #print('k_ssb, nid2, i_ssb\n',self.k_ssb, self.nid2, self.i_ssb)
                    output_items[2][n_items_produced][0] = self.i_ssb
                    output_items[0][n_items_produced][0] = self.nid2
                    output_items[1][n_items_produced][:] = self.memory.flatten(order='F')
                    n_items_produced += 1
                #return 1
                self.no_ssb_counter = 0
            else:
                self.no_ssb_counter +=1
                if self.no_ssb_counter >= self.reset:
                    #print(self.no_ssb_counter, self.reset, self.i_ssb)
                    #self.i_ssb = 0
                    self.no_ssb_counter = 0

        self.consume_each(len(samples))
        #consume(0, len(input_items[0]))
        return n_items_produced
