# ds_docker_cloudwatch


A python module that allows you to run a Docker container and stream its logs to AWS CloudWatch.


```bash
python main.py --docker-image newapp --bash-command 'pip install pip -U && pip install tqdm && python -c "import time; counter = 0; "' --aws-cw-group test_group_1 --aws-cw-stream test_stream_group1_1 --aws-access-key-id None --aws-secret-access-key None --aws-region us-east-1 --ports 8000 --only-start-log True

```


- docker-image: The name of the Docker image to be used
- bash-command: The command to be run inside the container
- aws-cw-group: The CloudWatch group name to use for logging
- aws-cw-stream: The CloudWatch stream name to use for logging
- aws-access-key-id: The AWS access key ID to use for CloudWatch
- aws-secret-access-key: The AWS secret access key to use for CloudWatch
- aws-region: The AWS region to use for CloudWatch
- ports: The ports to be exposed for the container
- only-start-log: A flag to set if only start logs should be sent to CloudWatch or stream logs.


Requirements:
- Docker must be installed on the machine 
- docker==6.0.1
- AWS credentials with permissions to create and write