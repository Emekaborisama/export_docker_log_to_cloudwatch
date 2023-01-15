# Python program to demonstrate
# command line arguments


import argparse
import subprocess
import os
import sys

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-di", "--docker_image", help = "Show Output")
parser.add_argument("-bc", "--bash_command", help = "Show Output")


# Read arguments from command line
args = parser.parse_args()

print(args.docker_image)
if args.docker_image:
    with open("Dockerfile", "w") as f:
        f.writelines("""FROM python:3.8 \nRUN mkdir /app \nWORKDIR /app \nADD . /app/ \nRUN pip install -r requirements.txt \nCMD ["python", "app.py"]\nEXPOSE 8000""")

if args.bash_command:
    with open("bash_script.sh", "w") as f:
        f.writelines("""""")

    # rc = subprocess.call("create_docker.sh")
