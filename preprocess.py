#  -*- coding: utf-8 -*-
# *********************************************************************
# Kafka Histogram Re-streamer
# Copyright (C) 2019 European Spallation Source ERIC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Module authors:
#   Michael Hart <michael.hart@stfc.ac.uk>
# *********************************************************************

# Special variables:
#   input  = reference to input workspace
#   output = name of the processed output workspace
# Temporary workspaces should be deleted

from mantid.simpleapi import Rebin, mtd
from config import rebin_params


# Comment in Mantid log
print 'Processing events into histogram'

# Just rebinning for now, but could do more
mtd[output] = Rebin(input, Params=rebin_params, PreserveEvents=False)
