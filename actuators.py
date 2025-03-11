import json
import paho.mqtt.client as mqtt
import time

# Lista de nós do cluster
BROKERS = ["rabbitmq1", "rabbitmq2", "rabbitmq3"]
BROKER_PORT = 1883
TOPIC = "actuators.command" 
STATE_TOPIC = "actuators.state"
RETRY_INTERVAL = 5

class Actuators:
    def __init__(self):
        self.client = None
        self.current_broker = None
        self.state = False
        self.connect()

    def connect(self):
        while True:
            for broker in BROKERS:
                try:
                    self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
                    self.client.on_message = self.on_message  # Define o callback para mensagens recebidas

                    self.client.connect(broker, BROKER_PORT, 60)
                    self.current_broker = broker
                    print(f"Conectado ao nó {broker}")

                    # Assina o tópico de comandos
                    self.client.subscribe(TOPIC, qos=2)
                    print(f"Inscrito no tópico {TOPIC}")

                    self.publish_state()
                    return
                except Exception as e:
                    print(f"Falha na conexão com {broker}: {str(e)}")
            print(f"Todas as conexões falharam. Tentando novamente em {RETRY_INTERVAL} segundos...")
            time.sleep(RETRY_INTERVAL)

    def on_message(self, client, userdata, msg):
        """Callback para processar mensagens recebidas."""
        try:
            payload = msg.payload.decode()
            command = json.loads(payload).get("command")

            if command in [True, False]:
                self.state = command  # Atualiza o estado
                print(f"Estado alterado para: {'ligado' if self.state else 'desligado'}")
                self.publish_state()
            else:
                print(f"Comando inválido recebido: {command}")
        except Exception as e:
            print(f"Erro ao processar mensagem: {str(e)}")

    def publish_state(self):
        try:
            state_message = {"state": self.state}
            self.client.publish(
                topic=STATE_TOPIC,
                payload=json.dumps(state_message),
                qos=2
            )
            print(f"Estado publicado: {state_message}")
        except Exception as e:
            print(f"Erro ao publicar estado: {str(e)}")

    def start(self):
        """Inicia o loop do cliente MQTT."""
        print(" [*] Aguardando comandos. Pressione CTRL+C para sair")
        self.client.loop_forever()

if __name__ == "__main__":
    actuators = Actuators()
    actuators.start()