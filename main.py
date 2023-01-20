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

container_id = "386b09caf32cb484c09b7ec6986f5e26a907b87f7424b0c30a4266f1d2274c93"
logs = subprocess.Popen(["docker", "logs", container_id], stdout=subprocess.PIPE)

log_events = {
        "timestamp": int(time.time()*1000),
        "message": logs.stdout.read()
    }



subprocess.run(["aws", "logs", "put-log-events", "--log-group-name", "test_group_1", "--log-stream-name", "test_stream_group1_1", "--region", "us-east-1", "--log-events", str(log_events)], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


# st.run("docker stop $(docker ps -q --filter ancestor=newapp:latest)")