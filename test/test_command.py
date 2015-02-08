#from unittest.mock import Mock
import unittest
#from mock import Mock
from py_shell.command import Command
#import subprocess
from pprint import pprint
from types import MethodType


class TestCommand(unittest.TestCase):
    def test_2(self):
        ls = LsCommand()
        ls.help().run()
        ls._register_options()

        print "\nls.run():"
        ls.help().run()

        fail

    def xtest_2(self):
        ls = LsCommand()
        ls2 = ls.literal()

        print "\nls.run():"
        ls.help().run()

        #print "\nls2.run():"
        #ls2.run()

        print "\nls2.help().run():"
        ls2.help().run()

        #rsync = RsyncCommand()
        #rsync.run()
        fail

    def xtest_copy_methods(self):
        t = Thing()

        def oi(self):
            print "hey"
        oi.__name__ = "hey"

        m = MethodType(oi, t)
        setattr(t, "hey", m)

        t.hey()

        ###########
        t2 = Thing()

        m = t.__dict__["hey"]
        print m
        t2.__dict__["hey"] = m

        t2.hey()
        fail


class Thing:
    pass


def option(func):
    print "@option: ", func
    return func


class LsCommand(Command):
    def __init__(self, pred=None, args=None):
        Command.__init__(self, binary="ls", parse_usage=True, pred=pred, args=args)

    #@option
    def help(self):
        print "############## good"
        self.args.append("--HELP")
        return self


class RsyncCommand(Command):
    def __init__(self):
        Command.__init__(self, binary="rsync", parse_usage=True)
