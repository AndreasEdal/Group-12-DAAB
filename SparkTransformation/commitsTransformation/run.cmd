docker build . -t CommitTransformation:latest 
docker run -ti --rm -e ENABLE_INIT_DAEMON=false --network big-data-network --name CommitTransformation CommitTransformation
