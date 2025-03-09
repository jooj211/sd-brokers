import json
import random
import time
import paho.mqtt.client as mqtt

BROKERS = ["rabbitmq1", "rabbitmq2", "rabbitmq3"]
BROKER_PORT = 1883
TOPIC = "sensors.data"
RETRY_INTERVAL = 5

class SensorClusterClient:
    def __init__(self):
        self.client = None
        self.current_broker = None
        self.connect()
    
    def connect(self):
        while True:
            for broker in BROKERS:
                try:
                    self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
                    self.client.username_pw_set("admin", "admin123")
                    self.client.connect(broker, BROKER_PORT, 60)
                    self.current_broker = broker
                    print(f"Conectado ao nó {broker}")
                    return
                except Exception as e:
                    print(f"Falha na conexão com {broker}: {str(e)}")
            
            print(f"Todas as conexões falharam. Tentando novamente em {RETRY_INTERVAL} segundos...")
            time.sleep(RETRY_INTERVAL)
    
    def publish_data(self):
        while True:
            sensor_data = {
                "sensor_id": random.randint(1, 100),
                "tipo": "temperatura" if random.random() > 0.5 else "umidade",
                "valor": random.uniform(20.0, 40.0),
                "timestamp": time.time(),
            }
            
            try:
                self.client.publish(
                    topic="sensors.data",
                    payload=json.dumps(sensor_data),
                    qos=2
                )
                print(f"Dado enviado para {self.current_broker}: {sensor_data}")
            except Exception as e:
                print(f"Erro ao publicar: {str(e)} - Tentando reconectar...")
                self.connect()
            
            time.sleep(random.uniform(0.5, 2.0))

if __name__ == "__main__":
    sensor = SensorClusterClient()
    sensor.publish_data()
