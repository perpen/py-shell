#from unittest.mock import Mock
import unittest
#from mock import Mock
from py_shell.command import Command, Rsync
#import subprocess
#from pprint import pprint


class TestCommand(unittest.TestCase):
    #def test_traditional(self):
        #subprocess.call(["ls", "-l"])
        #pass

    def test_rsync2(self):
        src = "./a"
        tgt = "./b"
        rsync = Rsync(src, tgt)
        rsync.params().verbose().run()
