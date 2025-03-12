FROM rabbitmq:3.8.34-management-alpine

# Instala o Keepalived e dependências
RUN apk add --no-cache keepalived

# Copia os arquivos de configuração do RabbitMQ
COPY rabbitmq.conf /etc/rabbitmq/
COPY .erlang.cookie /var/lib/rabbitmq/.erlang.cookie
RUN chmod 600 /var/lib/rabbitmq/.erlang.cookie

# Copia o script de entrada
COPY cluster-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/cluster-entrypoint.sh

# Habilita plugins do RabbitMQ
RUN rabbitmq-plugins enable --offline \
    rabbitmq_mqtt \
    rabbitmq_web_mqtt \
    rabbitmq_management

# Define o entrypoint
ENTRYPOINT ["/usr/local/bin/cluster-entrypoint.sh"]