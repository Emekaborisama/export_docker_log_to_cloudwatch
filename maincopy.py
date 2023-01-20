import argparse
import subprocess
import boto3
import time
import os
import docker

from multiprocessing import Process
# access_key = os.environ.get('AWS_ACCESS_KEY_ID')
# secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
# defualt_region = os.environ.get('AWS_REGION')

# print(defualt_region)


def get_docker_images():
    # Run the command
    result = subprocess.run(['docker', 'images'], stdout=subprocess.PIPE)
    # Decode the output
    output = result.stdout.decode()
    # Split the output by newline
    lines = output.split("\n")
    # Create an empty dictionary to store the images
    images = {}
    # Iterate over the lines of the output
    for line in lines[1:-1]:
        # Split the line by whitespace
        fields = line.split()
        # Get the image name and tag
        name = fields[0]
        tag = fields[1]
        # Add the image to the dictionary
        images[name] = tag
    return images


def is_bash_runnable(script_str):
    process = subprocess.Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate(input=script_str.encode())
    if process.returncode == 0:
        return True
    else:
        print(f"Error: {stderr.decode()}")
        return False


class dstack:
    def __init__(self, docker_image:str, bash_command:str,group_name:str, stream_name, aws_access_key_id,aws_secret_access_key,region,ports):
        self.docker_image = docker_image+":latest"
        self.bash_command = bash_command
        self.group_name = group_name
        self.stream_name = stream_name
        self.ports = ports+":"+ports+"/tcp"
        # self.defualt_region = defualt_region
        self.region = region 
        self.aws_access_key_id=aws_access_key_id
        self.aws_secret_access_key=aws_secret_access_key
        self.cloudwatch_client = boto3.client("logs", region_name =self.region,aws_access_key_id=self.aws_access_key_id,aws_secret_access_key=self.aws_secret_access_key)
    


    def dstack_docker_logs(self,container_run_id):
        
        # Run the command
        result = subprocess.run(['docker', 'logs','--details', container_run_id], stdout=subprocess.PIPE)
        # Decode the output
        output = result.stdout.decode()
        # Split the output by newline
        lines = output.split("\n")
        print(lines)
        return  lines


    


    def get_docker_logs(self, container_run_id):
        time.sleep(20)
        logs = subprocess.run(["docker", "logs", container_run_id], stdout=subprocess.PIPE)
        print(logs)
        # subprocess.run(["aws", "logs", "put-log-events", "--log-group-name", "test_group_1", "--log-stream-name", "test_stream_group1_1", "--region", "us-east-1", "--log-events", str(log_events)], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        
        return str(logs)

    


        

    def dstack_docker_run(self) -> bytes:
        # client = docker.from_env()
        # # run Docker container , 
        # container = client.containers.run(self.docker_image, self.bash_command,stdin_open=True,ports={"8000":"8000/tcp"}, detach=True)
        # return container"
        # run("docker ps -aq | xargs docker rm -f")
        # try:
        
        docker_ps = subprocess.run(["docker", "ps", "-q", "--filter", "ancestor="+self.docker_image], capture_output=True)
        docker_stop = subprocess.run(["docker", "stop"] + docker_ps.stdout.split())
        
        container_run_id = subprocess.run(["docker","run","--rm","-d","-t","-p",self.ports,self.docker_image], capture_output=True).stdout.strip()
        
        # subprocess.run(["docker", "exec", "-it",container_run_id,"bash","-c",str(self.bash_command)])
        print(container_run_id)
        return container_run_id
        # except subprocess.CalledProcessError as e:
        #     #validate if the docker image exist
        #     if self.docker_image in get_docker_images():
        #         return ("docker image is present in the images")
        #     elif is_runnable(script_str):
        #         return("The script is runnable and wouldn't return an error.")
        #     else:
        #         return ("Reecheck your AWS credentials")

        
        

    def run_docker_container(self) -> bytes:
        print("docker image",type(self.docker_image))
        container_run_id = self.dstack_docker_run()
        logs = self.get_docker_logs(container_run_id)
        self.send_logs_to_cloudwatch(logs)
        process = Process(target=self.send_logs_to_cloudwatch(logs))
        process.start()
        return logs






    def dstack_validate_and_create_client_group_and_streams(self):

        #validate if stream and group exist else create a new one
        try:
            self.cloudwatch_client.create_log_group(logGroupName=self.group_name)
        except self.cloudwatch_client.exceptions.ResourceAlreadyExistsException:
            pass

        # create log stream if it doesn't exist
        try:
            self.cloudwatch_client.create_log_stream(logGroupName=self.group_name, logStreamName=self.stream_name)
        except self.cloudwatch_client.exceptions.ResourceAlreadyExistsException:
            pass

        return self.cloudwatch_client













    



    def send_logs_to_cloudwatch(self, logs):
        def background_task():
            while True:
                self.cloudwatch_client.put_log_events(logGroupName=self.group_name, logStreamName=self.stream_name, logEvents=[
                {
                    "timestamp": int(time.time()*1000),
                    # "message": logs.stdout.read()
                    "message": logs
                }
            ])
                time.sleep(20) # update the logs to cloudwatch every 60 sec
        process = Process(target=background_task)
        process.start()


    # def send_logs_to_cloudwatch(self, logs):
    #     # send logs to CloudWatch
    #     # for log in logs:
    #     # print(logs)
    #     # self.cloudwatch_client.put_log_events(logGroupName=self.group_name, logStreamName=self.stream_name, logEvents=[
    #     #     {
    #     #         'timestamp': int(time.time() * 1000),
    #     #         'message': str("logs")
    #     #     },
    #     # ])
    #     self.cloudwatch_client.put_log_events(logGroupName=self.group_name, logStreamName=self.stream_name, logEvents=[
    #         {
    #             "timestamp": int(time.time()*1000),
    #             # "message": logs.stdout.read()
    #             "message": logs
    #         }
    #     ])
        # self.cloudwatch_client.put_log_events(logGroupName=self.group_name, logStreamName=self.stream_name, logEvents=["logs hello"])
        


    def run_container_and_send_logs_to_cloudwatch(self):
        # create CloudWatch log group and stream
        cloudwatch = self.dstack_validate_and_create_client_group_and_streams()

        # run Docker container
        logs = self.run_docker_container()
        #print(logs)

        # send logs to CloudWatch
        self.send_logs_to_cloudwatch(logs)


if __name__ == '__main__':
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--docker-image", required=True)
    parser.add_argument("--bash-command", required=True)
    parser.add_argument("--aws-client-group", required=True)
    parser.add_argument("--aws-client-stream", required=True)
    parser.add_argument("--aws-access-key-id", required=True)
    parser.add_argument("--aws-secret-access-key", required=True)
    parser.add_argument("--aws-region", required=True)
    parser.add_argument("--ports", required=True)
    args = parser.parse_args()
    dstack_run = dstack(docker_image = args.docker_image, bash_command =args.bash_command,
    group_name=args.aws_client_group, stream_name=args.aws_client_stream,aws_access_key_id=args.aws_access_key_id,aws_secret_access_key=args.aws_secret_access_key, region=args.aws_region,ports = args.ports)
    print(dstack_run.run_docker_container())
    # run_docker_container(docker_image=args.docker_image,args.bash_command)