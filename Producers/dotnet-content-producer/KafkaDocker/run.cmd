docker build . -t contentproducer:latest 
docker run -ti --rm -e ENABLE_INIT_DAEMON=false --network big-data-network --name contentproducer contentproducer
