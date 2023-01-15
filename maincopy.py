import argparse
import subprocess
import boto3



import os
access_key = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
region = os.environ.get('AWS_REGION')



class dstack:
    def __init__(self, docker_image:str, bash_command:str,group_name:str, stream_name, region):
        self.docker_image = docker_image
        self.bash_command = bash_command
        self.group_name = group_name
        self.stream_name = stream_name
        self.defualt_region =nonlocal region
        self.region = self.defualt_region if len(region) == None else region
        self.cloudwatch_client = boto3.client("logs", region_name =self.region)

    def run_docker_container(self) -> bytes:
        print("docker image",type(self.docker_image))
        container_run_id = self.dstack_docker_run(self.docker_image,self.bash_command)
        logs = self.dstack_docker_logs(container_run_id)
        return logs

    def dstack_docker_logs(self, container_run_id)-> bytes:
        logs = subprocess.run(["docker", "logs", container_run_id],capture_output=True).stdout
        return logs

    def dstack_docker_run(self) -> bytes:
        container_run_id = subprocess.run(["docker","run","-d",docker_image,bash_command], capture_output=True).stdout.strip()
        print("run type", type(container_run_id))
        return container_run_id






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
        





    def send_logs_to_cloudwatch(self, cloudwatch, logs):
        # send logs to CloudWatch
        for log in logs:
            cloudwatch.put_log_events(logGroupName=self.group_name, logStreamName=self.stream_name, logEvents=[
                {
                    'timestamp': int(time.time() * 1000),
                    'message': log
                },
            ])


    def run_container_and_send_logs_to_cloudwatch(access_key_id, secret_access_key):
        # create CloudWatch log group and stream
        cloudwatch = self.dstack_validate_and_create_client_group_and_streams()

        # run Docker container
        logs = self.run_docker_container()

        # send logs to CloudWatch
        send_logs_to_cloudwatch(cloudwatch, logs)


if __name__ == '__main__':
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--docker-image", required=True)
    parser.add_argument("--bash-command", required=True)
    parser.add_argument("--aws-client-group", required=True)
    parser.add_argument("--aws-client-stream", required=True)
    # parser.add_argument("--aws-access-key-id", required=False)
    # parser.add_argument("--aws-secret-access-key", required=False)
    parser.add_argument("--aws-region", required=False)
    args = parser.parse_args()
    dstack_run = dstack(docker_image = args.docker_image, bash_command =args.bash_command,
    group_name=args.aws_client_group, stream_name=args.aws_client_stream, region=args.aws_region)
    print(dstack_run)
    # run_docker_container(docker_image=args.docker_image,args.bash_command)