docker build . -t pysparkexampleimage:latest 
docker run -ti --rm -e ENABLE_INIT_DAEMON=false --network big-data-network --name pyspark pysparkexampleimage
