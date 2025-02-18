#!/bin/sh

rabbitmq-server -detached
sleep 15

if [ "$RABBITMQ_NODENAME" != "rabbit@rabbitmq1" ]; then
    until rabbitmqctl --node=rabbit@rabbitmq1 ping; do
        echo "Aguardando nó principal..."
        sleep 10
    done
    
    rabbitmqctl stop_app
    rabbitmqctl join_cluster rabbit@rabbitmq1
    rabbitmqctl start_app
fi

tail -f /dev/null