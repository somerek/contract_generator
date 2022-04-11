#!/bin/sh
cp ./.env.sample ./.env
chmod +x ./.env
. ./.env

docker-compose build --build-arg backend_host_port=$backend_host_port \
    --build-arg POSTGRES_USER=$POSTGRES_USER \
    --build-arg POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    --build-arg POSTGRES_DB=$POSTGRES_DB
docker-compose up -d

echo docker exec -it contract_db sh
echo "psql -U $POSTGRES_USER -d $POSTGRES_DB"
echo "\\dt;"
