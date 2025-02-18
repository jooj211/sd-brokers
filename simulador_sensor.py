import json
import random
import time

import paho.mqtt.client as mqtt

BROKER_HOST = "rabbitmq"
BROKER_PORT = 1883 
TOPIC = "sensors/data"

client = mqtt.Client()
client.connect(BROKER_HOST, BROKER_PORT)

while True:
    sensor_data = {
        "sensor_id": random.randint(1, 100),
        "tipo": "temperatura" if random.random() > 0.5 else "umidade",
        "valor": random.uniform(20.0, 40.0),
        "timestamp": time.time(),
    }

    client.publish(topic=TOPIC, payload=json.dumps(sensor_data))

    print(f"Dado enviado: {sensor_data}")
    time.sleep(random.uniform(0.5, 2.0))
