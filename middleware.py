import json
import paho.mqtt.client as mqtt
import time

# Lista de nós do cluster
BROKERS = ["rabbitmq1", "rabbitmq2", "rabbitmq3"]
BROKER_PORT = 1883
TOPIC = "sensors.data"

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f" [x] Recebido: {data}")
    except json.JSONDecodeError:
        print(" [!] Mensagem inválida recebida")

def connect_client():
    print("Conectando ao cluster...")
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    
    for broker in BROKERS:
        try:
            print(f"Tentando conectar em {broker}...")
            client.username_pw_set("admin", "admin123")
            client.connect(broker, BROKER_PORT, 60)
            client.subscribe(TOPIC, qos=2)
            print(f"Conectado ao nó {broker}")
            return client
        except Exception as e:
            print(f"Falha na conexão com {broker}: {str(e)}")
    
    raise Exception("Nenhum nó do cluster disponível")

def main():
    print('Middleware iniciado');
    while True:
        try:
            client = connect_client()
            print(" [*] Aguardando mensagens. Pressione CTRL+C para sair")
            client.loop_forever()
        except KeyboardInterrupt:
            print("\nConexão encerrada pelo usuário")
            break
        except Exception as e:
            print(f"Erro crítico: {str(e)} - Tentando reconectar em 5 segundos...")
            time.sleep(5)

if __name__ == "__main__":
    print('Middleware iniciado 22');
    main()