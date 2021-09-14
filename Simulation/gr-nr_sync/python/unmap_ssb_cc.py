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

class unmap_ssb_cc(gr.sync_block):
    """
    docstring for block unmap_ssb_cc
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="unmap_ssb_cc",
            in_sig=[(numpy.complex64, 4*240)],
            out_sig=[\
                (numpy.complex64,127),#sss
                (numpy.complex64,432),#pbch
                (numpy.complex64,144)])#dmrs


    def work(self, input_items, output_items):
        in0 = input_items[0]
        ssb = numpy.array(in0,dtype=complex).reshape(240,4)
        out = output_items[0]
        # <+signal processing here+>
        sss_data = nrSSB.unmap_sss(ssb)
        pbch_data, dmrs_data = nrSSB.unmap_pbch(ssb)
        out[0,:] = sss_data
        out[1,:] = pbch_data
        out[2,:] = dmrs_data
        return len(output_items[0])+len(output_items[1])+len(output_items[2])

