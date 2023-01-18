python maincopy.py --docker-image newapp --bash-command "pip install flask" --aws-client-group test_group_1 --aws-client-stream test_stream_group1_1 --aws-access-key-id AKIA27P7LR53FGCACV53 --aws-secret-access-key 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 --aws-region us-east-1 --ports 8000


docker run --rm -it -d -p 8000:8000/tcp newapp:latest 




docker ps -aq | xargs docker rm -f
docker image prune