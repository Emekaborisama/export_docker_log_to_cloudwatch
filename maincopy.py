import argparse
import subprocess
import boto3



def run_docker_container(docker_image, bash_command) -> bytes:
    container_run_id = dstack_docker_run(docker_image,bash_command)
    logs = dstack_docker_logs(container_run_id)
    return logs

def dstack_docker_logs(container_run_id)-> bytes:
    logs = subprocess.run(["docker", "logs", container_run_id],capture_output=True).stdout
    print("log type", type(logs))
    return logs

def dstack_docker_run(docker_image,bash_command) -> bytes:

    container_run_id = subprocess.run(["docker","run","-d",docker_image,bash_command], capture_output=True).stdout.strip()
    print("run type", type(container_run_id))
    return container_run_id






def dstack_validate_and_create_client_group_and_streams(group_name, stream_name, region):
    client = boto3.client("logs", region_name =region)
    #validate if stream and group exist else create a new one
    try:
        client.create_log_group(logGroupName=group_name)
    except client.exceptions.ResourceAlreadyExistsException:
        pass

    # create log stream if it doesn't exist
    try:
        client.create_log_stream(logGroupName=group_name, logStreamName=stream_name)
    except client.exceptions.ResourceAlreadyExistsException:
        pass

    return client
    





def send_logs_to_cloudwatch(group_name, stream_name, logs):
    # send logs to CloudWatch
    for log in logs:
        client.put_log_events(logGroupName=group_name, logStreamName=stream_name, logEvents=[
            {
                'timestamp': int(time.time() * 1000),
                'message': log
            },
        ])


def run_container_and_send_logs_to_cloudwatch(docker_image, bash_command, group_name, stream_name, region, access_key_id, secret_access_key):
    # create CloudWatch log group and stream
    cloudwatch = create_cloudwatch_log_group_and_stream(group_name, stream_name, region, access_key_id, secret_access_key)

    # run Docker container
    logs = run_docker_container(docker_image,bash_command)

    # send logs to CloudWatch
    send_logs_to_cloudwatch(cloudwatch, group_name, stream_name, logs)


if __name__ == '__main__':
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--docker-image", required=True)
    parser.add_argument("--bash-command", required=True)
    parser.add_argument("--aws-client-group", required=True)
    parser.add_argument("--aws-client-stream", required=True)
    # parser.add_argument("--aws-access-key-id", required=True)
    # parser.add_argument("--aws-secret-access-key", required=True)
    # parser.add_argument("--aws-region", required=True)
    args = parser.parse_args()
    dstack_create_client_group_and_streams(args.aws_client_group, args.aws_client_stream)
    # run_docker_container(docker_image=args.docker_image,args.bash_command)