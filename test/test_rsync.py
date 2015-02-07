#from unittest.mock import Mock
import unittest
#from mock import Mock
from py_shell.command import Command, Rsync
#import subprocess
#from pprint import pprint


class TestRsync(unittest.TestCase):
    def test_rsync(self):
        src = "./a"
        tgt = "./b"
        rsync = Rsync(src, tgt)
        rsync.params().verbose().run()
