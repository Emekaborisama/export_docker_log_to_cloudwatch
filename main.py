# # import requests

# # url = "http://127.0.0.1:8000/"



# # r = requests.get(url)
# # print(r.status_code)

# import subprocess
# import docker

# text = subprocess.run(["docker", "images"],capture_output=True).stdout
# print(text)

import subprocess



def get_container_logs():
    logs = []
    result = subprocess.run(['docker', 'exec', 'cd6e16f662e5d7a9be14f41d0479011f7f4312808a3321c1e8ee81f068f3148c', 'cat', '/var/log/*'], stdout=subprocess.PIPE)
    logs = result.stdout.decode().strip().split('\n')
    return logs

# Usage
container_logs = get_container_logs()
print(container_logs)



