docker build dotnet-commits-producer/KafkaDocker/. -t commitproducer:latest 
docker build dotnet-content-producer/KafkaDocker/. -t contentproducer:latest 
docker build dotnet-language-producer/KafkaDocker/. t languageproducer:latest 

echo "Running Producers: Commit, Content & Language"
docker run -d  -ti --rm -e ENABLE_INIT_DAEMON=false --network big-data-network --name commitproducer commitproducer && \
docker run -d -ti --rm -e ENABLE_INIT_DAEMON=false --network big-data-network --name contentproducer contentproducer && \
docker run -ti --rm -e ENABLE_INIT_DAEMON=false --network big-data-network --name languageproducer languageproducer
echo "Producers are done"
