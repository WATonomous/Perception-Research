#!/bin/bash
FIXUID=$(id -u)
FIXGID=$(id -g)

> ".env"
echo "COMPOSE_PROJECT_NAME=perception-research-${USER}" >> ".env"
echo "FIXUID=$FIXUID" >> ".env"
echo "FIXGID=$FIXGID" >> ".env"