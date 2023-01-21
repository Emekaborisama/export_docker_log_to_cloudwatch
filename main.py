# # import requests

# # url = "http://127.0.0.1:8000/"



# # r = requests.get(url)
# # print(r.status_code)

# import subprocess
# import docker

# text = subprocess.run(["docker", "images"],capture_output=True).stdout
# print(text)

import subprocess



# def get_container_logs():
#     logs = []
#     result = subprocess.run(['docker', 'exec', 'cd6e16f662e5d7a9be14f41d0479011f7f4312808a3321c1e8ee81f068f3148c', 'cat', '/var/log/*'], stdout=subprocess.PIPE)
#     logs = result.stdout.decode().strip().split('\n')
#     return logs

# # Usage
# container_logs = get_container_logs()
# print(container_logs)

# def get_docker_images():
#     # Run the command
#     result = subprocess.run(['docker', 'logs', "297fd073c1f44bf8720ff760352293fa6f3307868d01fd87edc1e8186bffd936"], stdout=subprocess.PIPE)
#     # Decode the output
#     output = result.stdout.decode()
#     # Split the output by newline
#     lines = output.split("\n")
#     # Create an empty dictionary to store the images
#     images = {}
#     # Iterate over the lines of the output
#     for line in lines[1:-1]:
#         # Split the line by whitespace
#         fields = line.split()
#         # Get the image name and tag
#         name = fields[0]
#         tag = fields[1]
#         # Add the image to the dictionary
#         images[name] = tag
#     return output


# print(get_docker_images())
import subprocess
import time
import json


# docker_ps = subprocess.run(["docker", "ps", "-q", "--filter", "ancestor=newapp:latest"], capture_output=True)
# docker_stop = subprocess.run(["docker", "stop"] + docker_ps.stdout.split())



# log_events = {
#         "timestamp": int(time.time()*1000),
#         "message": logs.stdout.read()
#         }



# subprocess.run(["aws", "logs", "put-log-events", "--log-group-name", "test_group_1", "--log-stream-name", "test_stream_group1_1", "--region", "us-east-1", "--log-events", str(log_events)], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


# st.run("docker stop $(docker ps -q --filter ancestor=newapp:latest)")



# import json
# import time


# def get_logs_and_store(container_id):
    
#     logs = subprocess.Popen(["docker", "logs", container_id], stdout=subprocess.PIPE)
#     log_events = [
#         {
#             "timestamp": int(time.time()*1000),
#             "message": logs.stdout.read()
#         }
#     ]
#     print(log_events)

#     # subprocess.run(["aws", "logs", "put-log-events", "--log-group-name", "test_group_1", "--log-stream-name", "test_stream_group1_1", "--region", "us-east-1", "--log-events", str(log_events)], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


# get_logs_and_store("74ce6e3985edf3ee121c5cf42f4b43f7a955ad020f5d80059c2038ba26a2ee92")

# subprocess.Popen(["aws", "logs", "put-log-events", "--log-group-name", "test_group_1", "--log-stream-name", "test_stream_group1_1", "--region", "us-east-1", "--log-events", str(log_events)], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)



import docker
import boto3
from multiprocessing import Process
# client = docker.from_env()
# container_id= client.containers.run('newapp', ports={'8000/tcp': 8000}, detach=True)
# print(container_id)
# subprocess.run(["docker", "cp", "container_id:/path/to/logfile", "logfile"])

# import boto3
# from mypy_boto3_logs.client import CloudWatchLogsClient

# # Create a boto3 CloudWatch Logs client
# cloudwatch_logs = boto3.client('logs')
# # mypy_cloudwatch_logs = CloudWatchLogsClient(client_config=cloudwatch_logs)

# # Get the log group name and stream name
# log_group_name = 'test_group_1'
# log_stream_name = 'test_stream_group1_1'

# # Create the log group and log stream if they don't exist


# # Tail the Docker container logs and send them to CloudWatch in real-time
container_name = "4eae4a54008b22011745ffeaa62006fc3de539cc3e84adfc3eb928e75dd9c722"
# logs = subprocess.Popen(['docker', 'logs', '-f', container_name], stdout=subprocess.PIPE)
# for line in iter(logs.stdout.readline, b''):
#     cloudwatch_logs.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=[{'timestamp': int(time.time() * 1000), 'message': line.decode()}])



# docker run --log-driver=syslog --log-opt syslog-address=udp://logs3.papertrailapp.com:30134 newapp
import subprocess

with open("docker.log", "w") as f:
    subprocess.run(["docker", "logs", "-f", "6b70cdfb1ff6488652284e0943701b77931587178f1eb53314306a1389ca0872"], stdout=f)


# subprocess.run(["sudo", "su"])
# subprocess.run(["cat", "/var/lib/docker/containers/", container_name,"/",container_name+"-json",".log"])
