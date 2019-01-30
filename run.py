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

# Ensure Python will be able to import files in this directory
import sys, os
FILEPATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(FILEPATH)

from time import sleep
from mantid.simpleapi import StartLiveData
from config import kafka_server


StartLiveData(FromNow=True, FromTime=False, FromStartOfRun=False, UpdateEvery=5.0,
              Instrument="SANS2D", Listener="KafkaEventListener",
              Address=kafka_server, RunTransitionBehavior="Stop",
              PreserveEvents=True, AccumulationMethod="Add",
              OutputWorkspace="test", AccumulationWorkspace="accum",
              ProcessingScriptFilename=FILEPATH + "/preprocess.py",
              PostProcessingScriptFilename=FILEPATH + "/postprocess.py")

while True:
    sleep(1)
