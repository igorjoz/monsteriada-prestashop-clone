#!/bin/bash

docker compose -f docker-compose_local.yml up -d

sleep 10

docker exec -i $(docker ps --filter "name=admin-mysql_db" -q) mysql -uroot -pstudent BE_191711 < data/db.sql