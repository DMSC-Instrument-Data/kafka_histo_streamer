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
