docker build dotnet-commits-producer/KafkaDocker/. -t commitproducer:latest 
docker run -ti --rm -e ENABLE_INIT_DAEMON=false -e DAAB_KAFKA_URL="10.123.252.230:9092,10.123.252.197:9092,10.123.252.206:9092" --network big-data-network --name commitproducer commitproducer

docker build dotnet-content-producer/KafkaDocker/. -t contentproducer:latest 
docker run -ti --rm -e ENABLE_INIT_DAEMON=false -e DAAB_KAFKA_URL="10.123.252.230:9092,10.123.252.197:9092,10.123.252.206:9092" --network big-data-network --name contentproducer contentproducer

docker build dotnet-language-producer/KafkaDocker/. -t languageproducer:latest 
docker run -ti --rm -e ENABLE_INIT_DAEMON=false -e DAAB_KAFKA_URL="10.123.252.230:9092,10.123.252.197:9092,10.123.252.206:9092" --network big-data-network --name languageproducer languageproducer
