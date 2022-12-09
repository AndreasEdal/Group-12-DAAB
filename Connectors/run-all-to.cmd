echo "Building Docker Images"
docker build ./CommitConnector -t commitconnector:latest 
docker build ./ContentConnector -t contentconnector:latest 
docker build ./LanguageConnector -t languageconnector:latest 

echo "Starting Connectors for commit, content & language"
docker run -ti --rm -e ENABLE_INIT_DAEMON=false --network big-data-network --name commitconnector commitconnector && \
docker run -ti --rm -e ENABLE_INIT_DAEMON=false --network big-data-network --name contentconnector contentconnector && \
docker run -ti --rm -e ENABLE_INIT_DAEMON=false --network big-data-network --name languageconnector languageconnector 