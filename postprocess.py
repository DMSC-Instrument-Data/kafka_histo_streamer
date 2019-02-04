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
#   input  = reference to input workspace (accumulation WS)
#   output = name of the processed output workspace
# Temporary workspaces should be deleted

from pykafka import KafkaClient
from mantid.simpleapi import mtd
from serializer import Workspace2DSerializer
from config import kafka_server, kafka_topic


# We don't actually need to do anything to the data, so pass through
mtd[output] = input

fbconv = Workspace2DSerializer(input)
client = KafkaClient(hosts=kafka_server)
topic = client.topics[kafka_topic]

with topic.get_producer(use_rdkafka=True, sync=True, max_request_size=25000000) as producer:
    print 'Serializing histogram'
    producer.produce(fbconv.serialize())
