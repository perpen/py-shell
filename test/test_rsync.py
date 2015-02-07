#from unittest.mock import Mock
import unittest
#from mock import Mock
from py_shell.rsync import Rsync
#from pprint import pprint


class TestRsync(unittest.TestCase):
    def xtest_rsync(self):
        src = "./a"
        tgt = "./b"
        rsync = Rsync(src, tgt)
        rsync.params().verbose().run()
