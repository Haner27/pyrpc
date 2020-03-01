rm -rf /tmp/zookeeper
mkdir -p /tmp/zookeeper/data
docker run -d -p 2181:2181 -v /tmp/zookeeper/data:/data/ --name=zookeeper  --privileged zookeeper