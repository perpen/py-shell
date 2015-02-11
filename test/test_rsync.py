from mock import Mock, patch
import unittest
import subprocess
from py_shell.rsync import Rsync
from py_shell.command import CommandUsageError


class TestRsync(unittest.TestCase):

    def setUp(self):
        with open("test/rsync_usage.txt", "r") as f:
            out = f.read()
            self.usage_output = (out, "")

    @patch('py_shell.command.subprocess')
    def test_execution(self, mock_subprocess):
        output_tuples = [
            self.usage_output,
            ("out1", "err1"),
        ]
        self._setup_subprocess(mock_subprocess, output_tuples)

        rsync = Rsync().sources("/src1", "/src2").destination("/tgt")
        result = rsync.run()

        expected_result = ("out1", "err1")
        self.assertEqual(expected_result, result)
        expected_argv = ['rsync', '/src1', '/src2', '/tgt']
        self._assert_execution(mock_subprocess, expected_argv)

    @patch('py_shell.command.subprocess')
    def test_sources_validation(self, mock_subprocess):
        output_tuples = [
            self.usage_output,
            ("out1", "err1"),
        ]
        self._setup_subprocess(mock_subprocess, output_tuples)

        rsync = Rsync().destination("/tgt")
        self._assert_raises_msg(CommandUsageError, "missing params: sources",
                                rsync.run)

    @patch('py_shell.command.subprocess')
    def test_destination_validation(self, mock_subprocess):
        output_tuples = [
            self.usage_output,
            ("out1", "err1"),
        ]
        self._setup_subprocess(mock_subprocess, output_tuples)

        rsync = Rsync().sources("/src1", "/src2")
        self._assert_raises_msg(CommandUsageError, "missing params: destination",
                                rsync.run)

    def _setup_subprocess(self, mock_subprocess, output_tuples):
        mock_subprocess.PIPE = 1
        mock_popen_result = Mock()
        mock_popen_result.communicate.side_effect = output_tuples
        mock_popen = Mock()
        mock_popen.return_value = mock_popen_result
        mock_subprocess.Popen = mock_popen

    def _assert_execution(self, mock_subprocess, expected_argv):
        mock_subprocess.Popen.assert_called_with(expected_argv,
                                                 stderr=1, stdout=1)

    def _assert_raises_msg(self, error_class, error_msg, call, *args, **kwargs):
        try:
            call(*args, **kwargs)
        except BaseException as e:
            self.assertEqual(error_class, e.__class__)
            self.assertEqual(error_msg, e.args[0])
