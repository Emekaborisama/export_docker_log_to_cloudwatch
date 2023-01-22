import unittest
import subprocess
from ds_docker_cloudfront import dstack, validate_bcommand_dimage, is_bash_runnable, get_docker_images

class TestDstack(unittest.TestCase):
    def setUp(self):
        self.docker_image = "alpine:latest"
        self.bash_command = "echo hello world"
        self.cw_group_name = "test-group"
        self.cw_stream_name = "test-stream"
        self.aws_access_key_id = "test-access-key"
        self.aws_secret_access_key = "test-secret-key"
        self.region = "us-west-2"
        self.ports = 8000
        self.only_start_logs = False
        self.dstack_instance = dstack(self.docker_image, self.bash_command, self.cw_group_name, self.cw_stream_name, self.aws_access_key_id, self.aws_secret_access_key, self.region, self.ports, self.only_start_logs)

    def test_dstack_docker_run(self):
        # Test that the method returns a bytes object
        self.assertIsInstance(self.dstack_instance.dstack_docker_run(), bytes)

    def test_dstack_docker_logs(self):
        container_run = self.dstack_instance.dstack_docker_run()
        # Test that the method returns a string
        self.assertIsInstance(self.dstack_instance.dstack_docker_logs(container_run), str)

    def test_run_docker_container(self):
        # Test that the method returns a string
        self.assertIsInstance(self.dstack_instance.run_docker_container(), str)