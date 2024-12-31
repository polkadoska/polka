#!/bin/bash

docker-compose -f /root/docker-compose.yml stop bot
docker-compose -f /root/docker-compose.yml up  -d --build --force-recreate  bot
