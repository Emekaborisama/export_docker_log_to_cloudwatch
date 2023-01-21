python maincopy.py --docker-image newapp --bash-command "pip install flask" --aws-client-group test_group_1 --aws-client-stream test_stream_group1_1 --aws-access-key-id AKIA27P7LR53CNFP5WHD --aws-secret-access-key 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 --aws-region us-east-1 --ports 8000

# python maincopy.py --docker-image newapp --bash-command "pip install flask" --aws-client-group test_group_1 --aws-client-stream test_stream_group1_1 --aws-access-key-id ASIA27P7LR53DXNK6YFH --aws-secret-access-key v4vw29bLsE03w52WuUf0o1LTtu4oRoUjhcEEySov --aws-region us-east-1 --ports 8000

docker run --rm -it -d -p 8000:8000/tcp newapp:latest 





docker ps -aq | xargs docker rm -f
docker image prune
docker rmi newapp

{
  "log-driver": "gelf",
  "log-opts": {
    "gelf-address": "udp://1.2.3.4:12201"
  }
}