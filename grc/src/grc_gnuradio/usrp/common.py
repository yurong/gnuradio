# Copyright 2009 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import sys
from gnuradio import usrp, gr

##################################################
# Set frequency function w/ verbose option
##################################################
def set_frequency(u, which, subdev, frequency, verbose=False):
	"""
	Set the carrier frequency for the given subdevice.
	@param u the usrp source/sink
	@param which specifies the DDC/DUC number
	@param frequency the carrier frequency in Hz
	@param verbose if true, print usrp tuning information
	"""
	r = u.tune(which, subdev, frequency)
	if not verbose: return
	print subdev.side_and_name()
	if r:
		print "\tr.baseband_frequency =", r.baseband_freq
		print "\tr.dxc_frequency =", r.dxc_freq
		print "\tr.residual_frequency =", r.residual_freq
		print "\tr.inverted =", r.inverted, "\n"
	else: print >> sys.stderr, 'Error calling tune on subdevice.'

##################################################
# Classes to associate usrp constructor w/ io size
##################################################
class usrp_helper(object):
	def _get_usrp_constructor(self): return self._usrp_args[0]
	def _get_io_size(self): return self._usrp_args[1]
class usrp_source_c(usrp_helper): _usrp_args = (usrp.source_c, gr.sizeof_gr_complex)
class usrp_source_s(usrp_helper): _usrp_args = (usrp.source_s, gr.sizeof_short)
class usrp_sink_c(usrp_helper): _usrp_args = (usrp.sink_c, gr.sizeof_gr_complex)
class usrp_sink_s(usrp_helper): _usrp_args = (usrp.sink_s, gr.sizeof_short)

##################################################
# RX antenna definitions and helpers
##################################################
def is_flex(rx_ant): return rx_ant.upper() in ('TX/RX', 'RX2')
def to_spec(side, rx_ant='RXA'):
	"""
	Convert the side to a spec number.
	@param side A or B
	@param rx_ant antenna type
	@return the spec (0/1, 0/1)
	"""
	try: return (
		{'A': 0, 'B': 1}[side.upper()], #side spec is 0 for A, 1 for B
		rx_ant.upper() == 'RXB' and 1 or 0, #subdev spec is 1 for RXB
	)
	except: raise ValueError, 'Side A or B expected.'