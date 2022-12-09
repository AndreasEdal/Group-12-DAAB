echo "Starting building docker images"
docker build commitsTransformation/. -t committransformation:latest 
docker build contentTransformation/. -t contenttransformation:latest 
docker build languageTransformation/. -t pysparktransformation:latest 

echo "running commit, content & pyspark transformation"
docker run -ti --rm -e ENABLE_INIT_DAEMON=false --network big-data-network --name committransformation committransformation && \
docker run -ti --rm -e ENABLE_INIT_DAEMON=false --network big-data-network --name contenttrans contenttransformation && \
docker run -ti --rm -e ENABLE_INIT_DAEMON=false --network big-data-network --name pyspark pysparktransformation





