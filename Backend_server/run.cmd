docker build . -t pyflaskwebserver:latest 
docker run -p 7050:7050 -ti --rm -e ENABLE_INIT_DAEMON=false --network big-data-network --name pyspark pyflaskwebserver
