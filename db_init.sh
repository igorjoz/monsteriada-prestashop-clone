#!/bin/bash

# docker stack deploy -c docker-compose.yml BE_191711 --with-registry-auth

docker exec -i $(docker ps --filter "name=admin-mysql_db" -q) mysql -uroot -pstudent BE_191711 < ./db.sql