from kafka.errors import KafkaError
from kafka.producer.kafka import *

import json

producer = KafkaProducer(bootstrap_servers='172.31.29.77:9092')

article = {
    'source': 'newsy',
    'logo': 'https://s3-us-west-1.amazonaws.com/ottoradio.image.source/newsy.png',
    'sourceTitle': 'Newsy',
    'trackId': 'newsy-7687',
    'playUrl': 'http://9cf6a87f38f28effb06b-fdf3de149acbb4f582e72737617b4a3b.r23.cf1.rackcdn.com/74660_1513882580.low.mp3',
    'intro': 'Gadell\'s Processing, located in Virginia, has donated about 50,000 pounds of venison to SERVE\'s food pantry through Hunters for the Hungry. The charity aims to provide meat to those in need.',
    'title': 'Hunters Keep Food Pantries And Stomachs Full',
    'trackCover': 'http://newsymain.npgroup.netdna-cdn.com/images/videos/m/1513881935.jpg',
}
i = 0
while i < 10000:
    future = producer.send('otto_content', key=b'test', value=json.dumps(article))
    i += 1
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError as e:
        # Decide what to do if produce request failed...
        pass
    # Successful result returns assigned partition and offset
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

producer.flush()
