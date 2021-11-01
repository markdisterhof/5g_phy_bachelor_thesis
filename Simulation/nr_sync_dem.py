#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: 5G NR Synchronization Procedure Demo
# Author: Mark Disterhof
# Copyright: Mark Disterhof
# GNU Radio version: 3.9.3.0

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
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import nr_phy_sync
import nr_sync



from gnuradio import qtgui

class nr_sync_dem(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "nr_sync_dem")

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
        self.shared_spectr = shared_spectr = True
        self.paired_spectr = paired_spectr = False
        self.mu = mu = 0
        self.f = f = 100000
        self.N_RB = N_RB = 30
        self.num_carr = num_carr = N_RB *12
        self.idxs = idxs = nr_phy_sync.nrSSB.get_ssb_idxs(nr_phy_sync.nrSSB.get_ssb_candidate_idx(mu, f, shared_spectr, paired_spectr), mu, shared_spectr)
        self.threshold = threshold = 0.9
        self.samp_rate = samp_rate = 20000
        self.pbch_data = pbch_data = [0]
        self.num_cp = num_cp = num_carr//4
        self.k_ssb = k_ssb = 10
        self.N_ID2 = N_ID2 = 2
        self.N_ID1 = N_ID1 = 321
        self.L__max = L__max = len(idxs)

        ##################################################
        # Blocks
        ##################################################
        self._threshold_range = Range(0.0, 1.0, 0.01, 0.9, 200)
        self._threshold_win = RangeWidget(self._threshold_range, self.set_threshold, 'threhold', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._threshold_win)
        self.qtgui_time_raster_sink_x_0_1 = qtgui.time_raster_sink_f(
            samp_rate,
            50,
            num_carr,
            [],
            [],
            "Tx Resourcegrid",
            1,
            None
        )

        self.qtgui_time_raster_sink_x_0_1.set_update_time(0.10)
        self.qtgui_time_raster_sink_x_0_1.set_intensity_range(-1, 1)
        self.qtgui_time_raster_sink_x_0_1.enable_grid(False)
        self.qtgui_time_raster_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_time_raster_sink_x_0_1.set_x_label("")
        self.qtgui_time_raster_sink_x_0_1.set_x_range(0.0, 0.0)
        self.qtgui_time_raster_sink_x_0_1.set_y_label("")
        self.qtgui_time_raster_sink_x_0_1.set_y_range(0.0, 0.0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_raster_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_raster_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_time_raster_sink_x_0_1.set_color_map(i, colors[i])
            self.qtgui_time_raster_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_raster_sink_x_0_1_win = sip.wrapinstance(self.qtgui_time_raster_sink_x_0_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_raster_sink_x_0_1_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_raster_sink_x_0 = qtgui.time_raster_sink_f(
            samp_rate,
            50,
            num_carr,
            [],
            [],
            "Rx Resourcegrid",
            1,
            None
        )

        self.qtgui_time_raster_sink_x_0.set_update_time(0.10)
        self.qtgui_time_raster_sink_x_0.set_intensity_range(-1, 1)
        self.qtgui_time_raster_sink_x_0.enable_grid(False)
        self.qtgui_time_raster_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_raster_sink_x_0.set_x_label("")
        self.qtgui_time_raster_sink_x_0.set_x_range(0.0, 0.0)
        self.qtgui_time_raster_sink_x_0.set_y_label("")
        self.qtgui_time_raster_sink_x_0.set_y_range(0.0, 0.0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_raster_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_raster_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_raster_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_time_raster_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_raster_sink_x_0_win = sip.wrapinstance(self.qtgui_time_raster_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_raster_sink_x_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
            240*4, #size
            "Rx SSB Constellation", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0.enable_grid(True)
        self.qtgui_const_sink_x_0_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_0_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            num_carr, #size
            "Rx Constellation", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.nr_sync_unmap_ssb_cc_0 = nr_sync.unmap_ssb_cc((N_ID2 + 3* N_ID1)%4)
        self.nr_sync_sss_decode_ci_0 = nr_sync.sss_decode_ci()
        self.nr_sync_rgrid_c_0 = nr_sync.rgrid_c(N_RB, N_ID1, N_ID2, k_ssb, mu, f, pbch_data, shared_spectr, paired_spectr)
        self.nr_sync_pss_detector_cc_0 = nr_sync.pss_detector_cc(N_RB, L__max, threshold)
        self.nr_sync_pbch_descramble_ci_0 = nr_sync.pbch_descramble_ci(L__max)
        self.nr_sync_nidcell_ii_0 = nr_sync.nidcell_ii()
        self.blocks_vector_to_stream_0_2 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, num_carr)
        self.blocks_vector_to_stream_0_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, num_carr)
        self.blocks_vector_to_stream_0_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 240*4)
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, num_carr)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, num_carr)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*num_carr, 200,True)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, num_carr)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, num_carr)
        self.blocks_stream_to_tagged_stream_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_gr_complex, num_carr, 1, "packet_len")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_gr_complex, num_carr, 1, "packet_len")
        self.blocks_null_sink_1_0 = blocks.null_sink(gr.sizeof_int*864)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_gr_complex*144)
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.qtgui_time_raster_sink_x_0, 0))
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.qtgui_time_raster_sink_x_0_1, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_vector_to_stream_0_1, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0, 0), (self.blocks_vector_to_stream_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0, 0), (self.nr_sync_pss_detector_cc_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_vector_to_stream_0_2, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.blocks_stream_to_tagged_stream_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0_0, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_1, 0), (self.blocks_complex_to_real_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_2, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.nr_sync_nidcell_ii_0, 0), (self.nr_sync_pbch_descramble_ci_0, 0))
        self.connect((self.nr_sync_pbch_descramble_ci_0, 0), (self.blocks_null_sink_1_0, 0))
        self.connect((self.nr_sync_pss_detector_cc_0, 1), (self.blocks_vector_to_stream_0_0_0, 0))
        self.connect((self.nr_sync_pss_detector_cc_0, 0), (self.nr_sync_nidcell_ii_0, 0))
        self.connect((self.nr_sync_pss_detector_cc_0, 0), (self.nr_sync_sss_decode_ci_0, 0))
        self.connect((self.nr_sync_pss_detector_cc_0, 2), (self.nr_sync_unmap_ssb_cc_0, 1))
        self.connect((self.nr_sync_pss_detector_cc_0, 1), (self.nr_sync_unmap_ssb_cc_0, 0))
        self.connect((self.nr_sync_rgrid_c_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.nr_sync_sss_decode_ci_0, 0), (self.nr_sync_nidcell_ii_0, 1))
        self.connect((self.nr_sync_unmap_ssb_cc_0, 3), (self.blocks_null_sink_1, 0))
        self.connect((self.nr_sync_unmap_ssb_cc_0, 2), (self.nr_sync_pbch_descramble_ci_0, 2))
        self.connect((self.nr_sync_unmap_ssb_cc_0, 1), (self.nr_sync_pbch_descramble_ci_0, 1))
        self.connect((self.nr_sync_unmap_ssb_cc_0, 0), (self.nr_sync_sss_decode_ci_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "nr_sync_dem")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_shared_spectr(self):
        return self.shared_spectr

    def set_shared_spectr(self, shared_spectr):
        self.shared_spectr = shared_spectr
        self.set_idxs(nr_phy_sync.nrSSB.get_ssb_idxs(nr_phy_sync.nrSSB.get_ssb_candidate_idx(self.mu, self.f, self.shared_spectr, self.paired_spectr), self.mu, self.shared_spectr))

    def get_paired_spectr(self):
        return self.paired_spectr

    def set_paired_spectr(self, paired_spectr):
        self.paired_spectr = paired_spectr
        self.set_idxs(nr_phy_sync.nrSSB.get_ssb_idxs(nr_phy_sync.nrSSB.get_ssb_candidate_idx(self.mu, self.f, self.shared_spectr, self.paired_spectr), self.mu, self.shared_spectr))

    def get_mu(self):
        return self.mu

    def set_mu(self, mu):
        self.mu = mu
        self.set_idxs(nr_phy_sync.nrSSB.get_ssb_idxs(nr_phy_sync.nrSSB.get_ssb_candidate_idx(self.mu, self.f, self.shared_spectr, self.paired_spectr), self.mu, self.shared_spectr))

    def get_f(self):
        return self.f

    def set_f(self, f):
        self.f = f
        self.set_idxs(nr_phy_sync.nrSSB.get_ssb_idxs(nr_phy_sync.nrSSB.get_ssb_candidate_idx(self.mu, self.f, self.shared_spectr, self.paired_spectr), self.mu, self.shared_spectr))

    def get_N_RB(self):
        return self.N_RB

    def set_N_RB(self, N_RB):
        self.N_RB = N_RB
        self.set_num_carr(self.N_RB *12)

    def get_num_carr(self):
        return self.num_carr

    def set_num_carr(self, num_carr):
        self.num_carr = num_carr
        self.set_num_cp(self.num_carr//4)
        self.blocks_multiply_const_xx_0.set_k(1/self.num_carr)
        self.qtgui_time_raster_sink_x_0.set_num_cols(self.num_carr)
        self.qtgui_time_raster_sink_x_0_1.set_num_cols(self.num_carr)

    def get_idxs(self):
        return self.idxs

    def set_idxs(self, idxs):
        self.idxs = idxs
        self.set_L__max(len(self.idxs))

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

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




def main(top_block_cls=nr_sync_dem, options=None):

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
