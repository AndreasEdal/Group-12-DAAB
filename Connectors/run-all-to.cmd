docker build ./CommitConnector -t commitconnector:latest
docker build ./ContentConnector -t contentconnector:latest
docker build ./LanguageConnector -t languageconnector:latest

docker run -ti --rm -e ENABLE_INIT_DAEMON=false -e --network big-data-network --name commitconnector commitconnector && \
docker run -ti --rm -e ENABLE_INIT_DAEMON=false -e --network big-data-network --name contentconnector contentconnector && \
docker run -ti --rm -e ENABLE_INIT_DAEMON=false -e --network big-data-network --name languageconnector languageconnector 


