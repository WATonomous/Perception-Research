#!/bin/bash
FIXUID=$(id -u)
FIXGID=$(id -g)
BASE_PORT=${BASE_PORT:-$(($(id -u)*20))}
GUI_TOOLS_VNC_PORT=${GUI_TOOLS_VNC_PORT:-$((BASE_PORT++))}

echo "COMPOSE_PROJECT_NAME=perception-research-${USER}" >> ".env"
echo "FIXUID=$FIXUID" >> ".env"
echo "FIXGID=$FIXGID" >> ".env"
echo "GUI_TOOLS_VNC_PORT=$GUI_TOOLS_VNC_PORT" >> ".env"