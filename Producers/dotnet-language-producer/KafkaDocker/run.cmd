docker build . -t languageproducer:latest 
docker run -ti --rm -e ENABLE_INIT_DAEMON=false -e DAAB_KAFKA_URL="10.123.252.230:9092,10.123.252.197:9092,10.123.252.206:9092" --network big-data-network --name languageproducer languageproducer
