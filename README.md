```markdown
# Sistema de Monitoramento de Sensores via MQTT

Um sistema distribuído para simulação de sensores (temperatura/umidade) e coleta de dados via protocolo MQTT, utilizando o broker Mosquitto.

## 📋 Funcionalidades
- **Protocolo MQTT**: Comunicação leve e eficiente para IoT.
- **Simulação de Sensores**: Geração automática de dados aleatórios.
- **Middleware**: Recebe e processa dados em tempo real.
- **Docker Support**: Opcional para containerização (veja seção abaixo).

## 🛠️ Pré-requisitos
- Python 3.8+
- Broker MQTT (Mosquitto)
- Pacotes Python: `paho-mqtt`

## 🔧 Instalação

### 1. Configurar o Broker Mosquitto
#### Windows:
1. Baixe o [Mosquitto](https://mosquitto.org/download/)
2. Inicie o serviço:
   ```powershell
   net start mosquitto
   ```

#### WSL/Ubuntu:
```bash
sudo apt-get install mosquitto mosquitto-clients
sudo service mosquitto start
```

### 2. Instalar Dependências
```bash
pip install paho-mqtt
```

## ⚙️ Configuração
Edite os seguintes parâmetros nos arquivos se necessário:
```python
# middleware_mqtt.py e simulador_sensor_mqtt.py
BROKER_HOST = "localhost"  # Use o IP do host se o broker estiver em outra máquina
BROKER_PORT = 1883
TOPIC = "sensors/data"
```

## 🚀 Uso
1. **Inicie o Middleware (Subscriber):**
   ```bash
   python middleware_mqtt.py
   ```

2. **Execute o Simulador de Sensores (Publisher):**
   ```bash
   python simulador_sensor_mqtt.py
   ```

3. **Teste Manual via CLI:**
   ```bash
   # Subscrever
   mosquitto_sub -h localhost -t "sensors/data"

   # Publicar
   mosquitto_pub -h localhost -t "sensors/data" -m '{"sensor_id": 1, "valor": 30.5}'
   ```

## 🐳 Docker (Opcional)
1. **Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   RUN pip install paho-mqtt
   COPY . /app
   WORKDIR /app
   ```

2. **Executar com Docker Compose:**
   ```yaml
   version: '3'
   services:
     broker:
       image: eclipse-mosquitto
       ports:
         - "1883:1883"
         
     middleware:
       build: .
       command: python middleware_mqtt.py
       depends_on:
         - broker
   ```
   ```bash
   docker-compose up
   ```

## 🔍 Solução de Problemas
- **Conexão Recusada:** Verifique se o broker está ativo e as portas 1883/9001 estão abertas.
- **Mensagens Não Entregues:** Confira o tópico e QoS (`qos=1` para entrega garantida).
- **Erros de Serialização:** Valide o formato JSON das mensagens.

## 📄 Licença
MIT License - Consulte o arquivo [LICENSE](LICENSE) para detalhes.

---

**Contribuições são bem-vindas!**  
📧 Contato: [seu-email@example.com] | 💬 Issues: [Reportar Problema](https://github.com/seu-usuario/repo/issues)
```

Este README fornece:  
- Instruções claras para diferentes ambientes (Windows/WSL)  
- Exemplos de uso direto  
- Opção de containerização  
- Troubleshooting básico  
- Seção de contribuição padrão  

Personalize os campos de contato e licença conforme necessário! 😊
