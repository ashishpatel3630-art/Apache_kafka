echo "Creating demo-topic..."

kafka-topics.sh 
--create 
--topic demo-topic 
--bootstrap-server localhost:9092 
--partitions 3 
--replication-factor 1

echo ""
echo "Available topics:"

kafka-topics.sh 
--list 
--bootstrap-server localhost:9092
