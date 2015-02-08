import unittest
from py_shell.rsync import Rsync


class TestRsync(unittest.TestCase):

    def test_1(self):
        rsync = Rsync()

        rsync.sources("/src1", "/src2").destination("/tgt")

        self.assertEqual(["rsync"], rsync.argv())
        print rsync.run()
        fail
