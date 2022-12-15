docker build commitsTransformation/. -t committransformation:latest 
docker build contentTransformation/. -t contenttransformation:latest 
docker build languageTransformation/. -t languagetransformation:latest 

docker run -d -ti --rm -e ENABLE_INIT_DAEMON=false --network big-data-network --name committransformation committransformation && \
docker run -d -ti --rm -e ENABLE_INIT_DAEMON=false --network big-data-network --name contenttransformation contenttransformation && \
docker run -d -ti --rm -e ENABLE_INIT_DAEMON=false --network big-data-network --name languagetransformation languagetransformation

