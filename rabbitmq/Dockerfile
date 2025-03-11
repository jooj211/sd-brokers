FROM rabbitmq:3.8.34-management-alpine

# Instalar Keepalived e dependências
RUN apk add --no-cache keepalived

# Copiar configurações do RabbitMQ
COPY rabbitmq.conf /etc/rabbitmq/
COPY .erlang.cookie /var/lib/rabbitmq/.erlang.cookie
RUN chmod 600 /var/lib/rabbitmq/.erlang.cookie

# Copiar configurações do Keepalived e scripts
COPY definitions.json /etc/rabbitmq
COPY keepalived.conf /etc/keepalived/
COPY check_rabbitmq.sh /etc/keepalived/
RUN chmod +x /etc/keepalived/check_rabbitmq.sh

# Habilita plugins
RUN rabbitmq-plugins enable --offline \
    rabbitmq_mqtt \
    rabbitmq_web_mqtt \
    rabbitmq_management

# Entrypoint modificado para iniciar ambos serviços
COPY cluster-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/cluster-entrypoint.sh

ENTRYPOINT ["cluster-entrypoint.sh"]