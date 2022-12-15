echo "RUNNING PRODUCERS BITCH"
docker build dotnet-commits-producer/KafkaDocker/. -t commitproducer:latest
docker build dotnet-content-producer/KafkaDocker/.  -t contentproducer:latest
docker build dotnet-language-producer/KafkaDocker/.  -t languageproducer:latest

docker run -ti --rm -e ENABLE_INIT_DAEMON=false -e --network big-data-network --name commitproducer commitproducer 
docker run -ti --rm -e ENABLE_INIT_DAEMON=false -e --network big-data-network --name contentproducer contentproducer 
docker run -ti --rm -e ENABLE_INIT_DAEMON=false -e --network big-data-network --name languageproducer languageproducer 


