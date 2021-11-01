#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: 5G NR Synchronization Procedure Demo
# Author: Mark Disterhof
# Copyright: Mark Disterhof
# GNU Radio version: 3.9.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import nr_phy_sync
import nr_sync



from gnuradio import qtgui

class nr_sync_simulation(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "5G NR Synchronization Procedure Demo", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("5G NR Synchronization Procedure Demo")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "nr_sync_simulation")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.N_RB = N_RB = 40
        self.shared_spectr = shared_spectr = True
        self.paired_spectr = paired_spectr = False
        self.num_carr = num_carr = N_RB *12
        self.mu = mu = 1
        self.f = f = 0
        self.samp_rate = samp_rate = 100#32000//10
        self.pbch_data = pbch_data = [0]
        self.num_cp = num_cp = num_carr//4
        self.k_ssb = k_ssb = 0
        self.N_ID2 = N_ID2 = 1
        self.N_ID1 = N_ID1 = 0
        self.L__max = L__max = nr_phy_sync.nrSSB.get_ssb_candidate_idx(mu, f, shared_spectr, paired_spectr)

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            num_carr, #size
            window.WIN_RECTANGULAR, #wintype
            0, #fc
            samp_rate, #bw
            "Sync Resourcegrid", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(True)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-0.5, 1.5)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.nr_sync_generate_rgrid_c_0 = nr_sync.generate_rgrid_c(N_RB, N_ID1, N_ID2, k_ssb, mu, f, [0], True, False)
        self.fft_vxx_0 = fft.fft_vcc(num_carr, False, window.rectangular(num_carr), True, 1)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, num_carr)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*num_carr, samp_rate,True)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_gr_complex, num_carr, num_carr, "packet_len")



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.nr_sync_generate_rgrid_c_0, 0), (self.blocks_throttle_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "nr_sync_simulation")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_N_RB(self):
        return self.N_RB

    def set_N_RB(self, N_RB):
        self.N_RB = N_RB
        self.set_num_carr(self.N_RB *12)

    def get_shared_spectr(self):
        return self.shared_spectr

    def set_shared_spectr(self, shared_spectr):
        self.shared_spectr = shared_spectr
        self.set_L__max(nr_phy_sync.nrSSB.get_ssb_candidate_idx(self.mu, self.f, self.shared_spectr, self.paired_spectr))

    def get_paired_spectr(self):
        return self.paired_spectr

    def set_paired_spectr(self, paired_spectr):
        self.paired_spectr = paired_spectr
        self.set_L__max(nr_phy_sync.nrSSB.get_ssb_candidate_idx(self.mu, self.f, self.shared_spectr, self.paired_spectr))

    def get_num_carr(self):
        return self.num_carr

    def set_num_carr(self, num_carr):
        self.num_carr = num_carr
        self.set_num_cp(self.num_carr//4)
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.num_carr)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.num_carr)

    def get_mu(self):
        return self.mu

    def set_mu(self, mu):
        self.mu = mu
        self.set_L__max(nr_phy_sync.nrSSB.get_ssb_candidate_idx(self.mu, self.f, self.shared_spectr, self.paired_spectr))

    def get_f(self):
        return self.f

    def set_f(self, f):
        self.f = f
        self.set_L__max(nr_phy_sync.nrSSB.get_ssb_candidate_idx(self.mu, self.f, self.shared_spectr, self.paired_spectr))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_pbch_data(self):
        return self.pbch_data

    def set_pbch_data(self, pbch_data):
        self.pbch_data = pbch_data

    def get_num_cp(self):
        return self.num_cp

    def set_num_cp(self, num_cp):
        self.num_cp = num_cp

    def get_k_ssb(self):
        return self.k_ssb

    def set_k_ssb(self, k_ssb):
        self.k_ssb = k_ssb

    def get_N_ID2(self):
        return self.N_ID2

    def set_N_ID2(self, N_ID2):
        self.N_ID2 = N_ID2

    def get_N_ID1(self):
        return self.N_ID1

    def set_N_ID1(self, N_ID1):
        self.N_ID1 = N_ID1

    def get_L__max(self):
        return self.L__max

    def set_L__max(self, L__max):
        self.L__max = L__max




def main(top_block_cls=nr_sync_simulation, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
