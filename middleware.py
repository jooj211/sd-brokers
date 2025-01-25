# middleware_mqtt.py
import json

import paho.mqtt.client as mqtt

# Configurações MQTT
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "sensors/data"


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print(f" [x] Recebido: {data}")


client = mqtt.Client()
client.connect(BROKER_HOST, BROKER_PORT)
client.subscribe(TOPIC)
client.on_message = on_message

print(" [*] Aguardando mensagens. Para sair pressione CTRL+C")
client.loop_forever()
