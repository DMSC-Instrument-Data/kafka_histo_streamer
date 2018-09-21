# Special variables:
#   input  = reference to input workspace (accumulation WS)
#   output = name of the processed output workspace
# Temporary workspaces should be deleted

# Where should these come from?
kafka_server = '172.18.0.3:9092'
kafka_topic = 'SANS2D_eventSum'

# We don't actually need to do anything to the data
mtd[output] = input


from pykafka import KafkaClient
from serializer import Workspace2DSerializer


fbconv = Workspace2DSerializer(input)
client = KafkaClient(hosts=kafka_server)
topic = client.topics[kafka_topic]

with topic.get_producer(use_rdkafka=True, sync=True, max_request_size=25000000) as producer:
    print 'Serializing histogram'
    producer.produce(fbconv.serialize())
