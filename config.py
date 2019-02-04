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

# String containing "server:port" of Kafka Broker to connect to
kafka_server = "172.18.0.3:9092"

# Name of Kafka topic to publish output histogram schema to
# Note: Under current ESS convention this will always be INSTNAME_eventSum
kafka_topic = 'SANS2D_eventSum'

# Parameters to pass to Mantid's Rebin algorithm when converting to histogram
rebin_params = '0,10000,100000'
