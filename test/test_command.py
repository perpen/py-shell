#from unittest.mock import Mock
import unittest
#from mock import Mock
from py_shell.command import Command
#import subprocess
#from pprint import pprint


class TestCommand(unittest.TestCase):
    def test_1(self):
        ls = Command("/usr/bin/ls", parse_usage=True)
        ls.params().literal().run()
        ls = Command("ls", parse_usage=True)
        ls.params().literal().run()

    def test_2(self):
        ls = LsCommand()
        ls.literal().run()


class LsCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def run(self):
        pass

    def literal(self):
        print "parsing literal"


class LsCommandState(CommandState):
    def literal(self):
        self.sup.literal()
