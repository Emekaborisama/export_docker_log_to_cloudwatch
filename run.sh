python main.py --docker-image newapp --bash-command 'pip install pip -U && pip install tqdm && python -c "import time; counter = 0; "' --aws-cw-group test_group_1 --aws-cw-stream test_stream_group1_1 --aws-access-key-id None --aws-secret-access-key None --aws-region us-east-1 --ports 8000 --only-start-log True

