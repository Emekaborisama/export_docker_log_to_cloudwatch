import argparse
import subprocess
import boto3
import time
import os
import docker
from tqdm import tqdm
import threading
try:
    from ds_docker_2_cloudwatch.utils import validate_bcommand_dimage

except:
    from utils import validate_bcommand_dimage




class dstack:
    def __init__(self, docker_image:str, bash_command:str,cw_group_name:str, cw_stream_name, aws_access_key_id,aws_secret_access_key,region,ports,only_start_logs:bool):
        """
        Initialize the class with the following parameters:
        :param docker_image: str: The name of the Docker image to be used
        :param bash_command: str: The command to be run inside the container
        :param cw_group_name: str: The CloudWatch group name to use for logging
        :param cw_stream_name: str: The CloudWatch stream name to use for logging
        :param aws_access_key_id: str: The AWS access key ID to use for CloudWatch
        :param aws_secret_access_key: str: The AWS secret access key to use for CloudWatch
        :param region: str: The AWS region to use for CloudWatch
        :param ports: int: The ports to be exposed for the container
        :param only_start_logs: bool: flag to set if only start logs should be sent to cloudwatch or stream logs.
        """
        self.docker_image = docker_image
        self.bash_command = bash_command
        self.cw_group_name = cw_group_name
        self.cw_stream_name = cw_stream_name
        self.ports = ports
        self.region = region 
        self.aws_access_key_id=aws_access_key_id
        self.aws_secret_access_key=aws_secret_access_key
        self.only_start_logs=only_start_logs
        self.cloudwatch_client = boto3.client("logs", region_name =self.region,aws_access_key_id=self.aws_access_key_id,aws_secret_access_key=self.aws_secret_access_key)
    





    def get_docker_stream_logs(self, container_id):
        """
        Method that  stream logs of a container and sends them to CloudWatch.
        :param container_id: str: The container id of the running container
        """
        # Run the command
        def background_task(self):
            count_new=0
            while True:
                time.sleep(1)
                result = subprocess.run(["docker", "logs",container_id], capture_output = True,text = True)
                # split the output into lines
                # write each line to the file
                self.lines =str(result)
                
                if count_new==len(self.lines):
                    pass
                else:
                    count_new+=len(self.lines )
                    # save_res = lines.replace("", "*")
                    if len(self.lines)>=1:
                        # split the output into lines
                        self.lines  = self.lines .split("\n")
                        self.cloudwatch_client.put_log_events(logGroupName=self.cw_group_name, logStreamName=self.cw_stream_name, logEvents=[
                                {
                                    "timestamp": int(time.time()*1000),
                                    "message": str(self.lines )
                                }
                            ])
                    return self.lines
        # create a new thread and run the background task
        self.thread = threading.Thread(target=background_task)
        # set the thread as a daemon thread so that it will automatically exit when the main program is done
        self.thread.daemon = True
        self.thread.start()
    

    def d_stack_get_docker_logs_subprocess(self,container_run):
        """
        Retrieves logs from a running Docker container using the subprocess module.
        If the only_start_logs parameter is set to True, only the initial logs of the container will be returned.
        If the only_start_logs parameter is set to False, the method will also start a background thread to continuously 
        stream the logs to CloudWatch.
        :param container_run: The container object from the `dstack_docker_run` method
        :return: If only_start_logs is True, returns a string of the initial logs of the container.
                If only_start_logs is False, returns a string indicating that the log streaming process has started.
        """
        # Run the command
        time.sleep(10)
        result = subprocess.run(["docker", "logs",str(container_run.id)], capture_output = True,text = True)
        # split the output into lines
        # write each line to the file
        lines =str(result)
        if self.only_start_logs == True:
            return lines
        elif self.only_start_logs == False:
            self.container_id = container_run.id
            self.get_docker_stream_logs(self.container_id)
            # Start the `get_docker_stream_logs` method as a background process
            # self.log_process = subprocess.Popen(["python", "-c", f"from {__name__} import get_docker_stream_logs; get_docker_stream_logs('{self.container_run}')"], 
            #                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE,start_new_session=True)
            return ("stream logs running")
        

    # get container start logs 
    def dstack_docker_logs(self,container_run: object):
        """
        Retrieves logs from a running Docker container using the docker sdk.
        If the only_start_logs parameter is set to True, only the initial logs of the container will be returned.
        If the only_start_logs parameter is set to False, the method will also start a background thread to continuously 
        stream the logs to CloudWatch.
        :param container_run: The container object from the `dstack_docker_run` method
        :return: If only_start_logs is True, returns a string of the initial logs of the container.
                If only_start_logs is False, returns a string indicating that the log streaming process has started.
        """
        
        time.sleep(15)
        if self.only_start_logs == True:
            logs = container_run.logs(stdout=True, stderr=True)
            result_logs = logs.decode().strip()
            return result_logs
        elif self.only_start_logs == False:
            self.container_id = container_run.id
            self.get_docker_stream_logs(self.container_id)
            # # Start the `get_docker_stream_logs` method as a background process
            # self.log_process = subprocess.Popen(["python", "-c", f"from {__name__} import get_docker_stream_logs; get_docker_stream_logs('{self.container_id}')"], 
            #                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE,start_new_session=True)
            return ("stream logs running")
            
            
  
    def dstack_docker_run(self):
        """
        Runs a docker container from a specified image and run a bash command inside the container.
        """
        # Create a Docker client
        client = docker.from_env()
        # Stop any running container with the image name
        
        containers = client.containers.list(filters={"ancestor": self.docker_image, "status": "running"})
        for container in containers:
      
            try:
                if self.thread.is_alive():
                    print("Thread is running")
                else:
                    pass
                # terminate thread
                self.thread.join()
            except:
                pass
            container.stop()
        # {'8000/tcp': 8000}
        containers_run = client.containers.run(self.docker_image,ports={str(self.ports)+'/tcp':self.ports},detach=True)
        containers_run.exec_run(self.bash_command)
        return containers_run
    

        
        

    def run_docker_container(self):
        """
        Runs a docker container method, and returns the logs from the container.
        """
        container_run_id = self.dstack_docker_run()
        logs = self.dstack_docker_logs(container_run_id)
        #  if logs == none get logs from stream logs
        if logs ==None:
            logs = self.d_stack_get_docker_logs_subprocess(container_run_id)
        else:
            logs=logs
        return logs






    def dstack_validate_and_create_client_group_and_streams(self):
        """
        Validates if a CloudWatch log group and stream exist and creates them if they do not.
        """

        #validate if stream and group exist else create a new one
        try:
            self.cloudwatch_client.create_log_group(logGroupName=self.cw_group_name)
        except self.cloudwatch_client.exceptions.ResourceAlreadyExistsException:
                pass
        except self.cloudwatch_client.exceptions.ClientError:
                raise ValueError("Invalid credentials or region")
                

        # create log stream if it doesn't exist
        try:
            self.cloudwatch_client.create_log_stream(logGroupName=self.cw_group_name, logStreamName=self.cw_stream_name)
        except self.cloudwatch_client.exceptions.ResourceAlreadyExistsException:
                pass
        except self.cloudwatch_client.exceptions.ClientError:
                raise ValueError("Invalid credentials or region")
                

        return self.cloudwatch_client




    def send_logs_to_cloudwatch(self, logs):
        """
        Sends logs to the specified CloudWatch log group and stream.
        """
        
        try:
            self.cloudwatch_client.put_log_events(logGroupName=self.cw_group_name, logStreamName=self.cw_stream_name, logEvents=[
                {
                    "timestamp": int(time.time()*1000),
                    "message": logs
                }
            ])
        except:
            time.sleep(10)
            self.cloudwatch_client.put_log_events(logGroupName=self.cw_group_name, logStreamName=self.cw_stream_name, logEvents=[
                {
                    "timestamp": int(time.time()*1000),
                    "message": str(logs)
                }
            ])

    def run_container_and_send_logs_to_cloudwatch(self):
        with tqdm(total=20, desc="checking if cloudwatch group and stream exist", unit="  done") as pbar1:
            self.dstack_validate_and_create_client_group_and_streams()
            pbar1.update(100)
        with tqdm(total=30, desc="Running docker container", unit="  done") as pbar2:
            logs = self.run_docker_container()
            pbar2.update(100)
        with tqdm(total=50, desc="Sending logs to Cloudwatch", unit="  done") as pbar3:
            self.send_logs_to_cloudwatch(logs)
            pbar3.update(100)
            
        return ("completed")


        
        


if __name__ == '__main__':
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--docker-image", required=True)
    parser.add_argument("--bash-command", required=True)
    parser.add_argument("--aws-cw-group", required=True)
    parser.add_argument("--aws-cw-stream", required=True)
    parser.add_argument("--aws-access-key-id", required=True)
    parser.add_argument("--aws-secret-access-key", required=True)
    parser.add_argument("--aws-region", required=True)
    parser.add_argument("--ports", required=False)
    parser.add_argument("--only-start-logs", required=False)
    args = parser.parse_args()
    
    validate_bd = validate_bcommand_dimage(bash_command=args.bash_command,docker_image = args.docker_image)
    dstack_run = dstack(docker_image = args.docker_image, bash_command =args.bash_command,
        cw_group_name=args.aws_cw_group, cw_stream_name=args.aws_cw_stream,aws_access_key_id=args.aws_access_key_id,aws_secret_access_key=args.aws_secret_access_key, region=args.aws_region,ports = args.ports, only_start_logs=args.only_start_logs)
        
    dstack_run.run_container_and_send_logs_to_cloudwatch()

    
    
    
