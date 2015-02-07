#from unittest.mock import Mock
import unittest
#from mock import Mock
from py_shell.command import Command
#import subprocess
#from pprint import pprint


class TestCommand(unittest.TestCase):
    def test_1(self):
        #ls = Command("/usr/bin/ls_and-other.things", options=True)
        ls = Command("/usr/bin/ls", parse_usage=True)
        ls = Command("ls", parse_usage=True)
        ls.params().literal().run()
        fail
