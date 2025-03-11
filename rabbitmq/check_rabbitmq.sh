#!/bin/sh
if rabbitmqctl node_health_check > /dev/null 2>&1; then
    exit 0
else
    exit 1
fi