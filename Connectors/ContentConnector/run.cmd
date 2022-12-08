docker build . -t contentconnector:latest 
docker run -ti --rm -e ENABLE_INIT_DAEMON=false --network big-data-network --name contentconnector contentconnector
