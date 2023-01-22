import unittest
import subprocess
try:
    from ds_docker_2_cloudwatch.main import dstack
    from ds_docker_2_cloudwatch.utils import validate_bcommand_dimage

except:
    from main import dstack
    from utils import validate_bcommand_dimage
    
from unittest.mock import patch
import boto3


class TestDstack(unittest.TestCase):
    def test_init_missing_parameters(self):
        # Test for missing parameters
        with self.assertRaises(TypeError):
            dstack()
        with self.assertRaises(TypeError):
            dstack(docker_image='myimage')
        with self.assertRaises(TypeError):
            dstack(docker_image='myimage', bash_command='mycommand')
        with self.assertRaises(TypeError):
            dstack(docker_image='myimage', bash_command='mycommand', cw_group_name='mygroup')
        with self.assertRaises(TypeError):
            dstack(docker_image='myimage', bash_command='mycommand', cw_group_name='mygroup', cw_stream_name='mystream')
        with self.assertRaises(TypeError):
            dstack(docker_image='myimage', bash_command='mycommand', cw_group_name='mygroup', cw_stream_name='mystream', aws_access_key_id='accesskey')
        with self.assertRaises(TypeError):
            dstack(docker_image='myimage', bash_command='mycommand', cw_group_name='mygroup', cw_stream_name='mystream', aws_access_key_id='accesskey', aws_secret_access_key='secretkey')
        with self.assertRaises(TypeError):
            dstack(docker_image='myimage', bash_command='mycommand', cw_group_name='mygroup', cw_stream_name='mystream', aws_access_key_id='accesskey', aws_secret_access_key='secretkey', region='us-west-2')
        with self.assertRaises(TypeError):
            dstack(docker_image='myimage', bash_command='mycommand', cw_group_name='mygroup', cw_stream_name='mystream', aws_access_key_id='accesskey', aws_secret_access_key='secretkey', region='us-west-2', ports=8080)
            
    
    def test_invalid_aws_creds(self):
        with self.assertRaises(ValueError):
            dstack_run = dstack(docker_image="alpine:latest", bash_command='pip install flask', cw_group_name='mygroup', cw_stream_name='mystream', aws_access_key_id="aws_key", aws_secret_access_key="aws_secret_key", region='us-west-2', ports=8080, only_start_logs=True)
            dstack_run.dstack_validate_and_create_client_group_and_streams()
    



class TestValidateBCommandDImage(unittest.TestCase):
    def test_invalid_bash_command(self):
        bash_command = "invalid_command"
        docker_image = "alpine:latest"
        with self.assertRaises(ValueError):
            validate_bcommand_dimage(bash_command, docker_image)
            
    def test_invalid_docker(self):
        bash_command = "pip isntall flask"
        docker_image = None
        with self.assertRaises(ValueError):
            validate_bcommand_dimage(bash_command, docker_image)

 
if __name__ == '__main__':
    unittest.main(exit=False)