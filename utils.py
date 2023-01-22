

import subprocess
import time
import os

    
    
    
def get_docker_images():
    """
    Returns a dictionary of all available local docker images, with the image names as keys and their respective tags as values.
    """
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
    """
    Validates if a bash script is runnable and would not return an error when executed
    """
    process = subprocess.Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate(input=script_str.encode())
    if process.returncode == 0:
        return True
    else:
        return False
    

    
    

def validate_bcommand_dimage(bash_command:str,docker_image):
    """
    Validates the bash command and docker image before running the container.
    """
    if not isinstance(bash_command, str) or not bash_command:
        raise ValueError("bash_command should be a non-empty string")
    if is_bash_runnable(bash_command) == False:
        raise ValueError("The bash script isn't runnable and would likely return an error.")
    if docker_image in get_docker_images():
        pass
    else:
        raise ValueError("docker image isn't present in the images")