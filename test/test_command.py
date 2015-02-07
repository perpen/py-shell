#from unittest.mock import Mock
import unittest
#from mock import Mock
from py_shell.command import Command, CommandState
#import subprocess
#from pprint import pprint


class TestCommand(unittest.TestCase):
    def test_1(self):
        #ls = Command("/usr/bin/ls_and-other.things", options=True)
        ls = Command("/usr/bin/ls", parse_usage=True)
        ls.params().literal().run()
        ls = Command("ls", parse_usage=True)
        ls.params().literal().run()
        fail

    def xtest_2(self):
        pass


class LsCommand(CommandState):
    def literal(self):
        super(LsCommand, self).literal()
