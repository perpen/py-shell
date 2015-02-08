#from unittest.mock import Mock
import unittest
#from mock import Mock
from py_shell.command import Command
#import subprocess
from pprint import pprint
from types import MethodType


class TestCommand(unittest.TestCase):
    def test1(self):
        ls = LsCommand()
        self.assertEqual(["ls"], ls._argv())
        self.assertEqual(["ls", "--all"], ls.all()._argv())
        self.assertEqual(["ls", "--all", "--literal"], ls.all().literal()._argv())
        #fail

    def test2(self):
        ls = Command(binary="ls", parse_usage=True)
        ls_l = ls.l()
        ls_la = ls_l.a()
        self.assertEqual(["ls", "-l"], ls_l._argv())
        self.assertEqual(["ls", "-l", "-a"], ls_la._argv())
        self.assertEqual(["ls", "-l"], ls_l._argv())

    def xtest_2(self):
        ls = LsCommand()
        #ls.help().run()
        ls._register_options()

        print "\nls.run():"
        #ls.literal().help().run()
        ls.help().literal().run()

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
    def __init__(self, *args, **kwargs):
        Command.init(self, "ls", True, **kwargs)

    def __init__0(self, *args, **kwargs):
        kwargs.update(binary="ls", parse_usage=True)
        Command.__init__(self, **kwargs)

    def help(self):
        print "############## overriden help"
        return self._pass("help")


class RsyncCommand(Command):
    def __init__(self):
        Command.__init__(self, binary="rsync", parse_usage=True)
