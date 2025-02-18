import json
import paho.mqtt.client as mqtt

BROKER_HOST = "rabbitmq"
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
