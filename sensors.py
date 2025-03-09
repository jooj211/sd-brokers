import json
import random
import time
import paho.mqtt.client as mqtt
from datetime import datetime

BROKERS = ["rabbitmq1", "rabbitmq2", "rabbitmq3"]
BROKER_PORT = 1883
TOPIC = "sensors.data"
RETRY_INTERVAL = 5

# Mapeamento fixo de id_device para tipo (sem atuador)
DEVICE_TYPES = {
    1: "Temperatura",
    2: "Umidade",
    3: "Pressao",
    4: "Temperatura",
    5: "Umidade",
    6: "Pressao",
}

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
            id_circuit = random.randint(1, 4)  # ID do circuito (pode variar)
            id_device = random.randint(1, 6)   # ID do dispositivo (fixo para manter o tipo)
            tipo = DEVICE_TYPES[id_device]     # Obtém o tipo fixo do dispositivo
            
            # Gera o valor para sensores (não há mais atuador)
            valor = random.uniform(30, 40)  # Valor contínuo para sensores
            
            # Estrutura dos dados a serem enviados
            sensor_data = {
                "id": id_circuit,
                "device": {
                    "id": id_device,
                    "tipo": tipo,
                    "valor": valor,
                    "timestamp": datetime.now().isoformat(),
                }
            }
            
            try:
                self.client.publish(
                    topic=TOPIC,
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