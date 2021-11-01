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

    def __init__(self, nu):
        gr.sync_block.__init__(self,
                               name="unmap_ssb_cc",
                               in_sig=[(numpy.complex64, 4*240),
                                       (numpy.int32, (1,))],
                               out_sig=[
                                   (numpy.complex64, 127),  # sss
                                   (numpy.complex64, 432),  # pbch
                                   ((numpy.int32, (1,))),  # i_ssb
                                   (numpy.complex64, 144)])  # dmrs
        self.nu = nu

    def work(self, input_items, output_items):
        ssb_dim = {
            'l': 4,
            'k': 240,
            'nu': self.nu
        }

        in0 = input_items

        ssb = numpy.array(in0[0][0], dtype=complex).reshape((240, 4), order='F')

        out = output_items
        # <+signal processing here+>
        sss_data = nrSSB.unmap_sss(ssb)
        pbch_data, dmrs_data = nrSSB.unmap_pbch(ssb, ssb_dim)
        out[0][0] = sss_data
        out[1][0] = pbch_data
        out[2][0] = in0[1][0]
        out[3][0] = dmrs_data
        return 1
