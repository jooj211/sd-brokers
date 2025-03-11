FROM rabbitmq:3.8.34-management-alpine

COPY rabbitmq.conf /etc/rabbitmq/
COPY .erlang.cookie /var/lib/rabbitmq/.erlang.cookie
RUN chmod 600 /var/lib/rabbitmq/.erlang.cookie

# 1. Copia os arquivos primeiro
COPY definitions.json /etc/rabbitmq
COPY rabbitmq.conf /etc/rabbitmq/
COPY cluster-entrypoint.sh /usr/local/bin/
RUN cat /etc/rabbitmq/rabbitmq.conf

# 2. Define permissões do script
RUN chmod +x /usr/local/bin/cluster-entrypoint.sh

# 3. Habilita plugins
RUN rabbitmq-plugins enable --offline \
    rabbitmq_mqtt \
    rabbitmq_web_mqtt \
    rabbitmq_management

# 4. Define entrypoint
ENTRYPOINT ["/bin/sh", "/usr/local/bin/cluster-entrypoint.sh"]