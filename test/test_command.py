import unittest
from py_shell.command import Command, UsageParser, Option


class TestUsageParser(unittest.TestCase):
    def test_normal_usage_is_parsed_correctly(self):
        usage = """Blah
            -o, --output=OUTPUT Specifies output
            -v
        blah
        """

        actual_options = UsageParser().parse(usage)

        expected_options = {
            "o": Option("o", "-o", "Specifies output", "OUTPUT"),
            "output": Option("output", "--output", "Specifies output", "OUTPUT"),
            "v": Option("v", "-v", None, None),
        }
        self.assertEqual(tuple(expected_options), tuple(actual_options))

    def test_empty_usage_produces_no_options(self):
        usage = ""

        actual_options = UsageParser().parse(usage)

        expected_options = {}
        self.assertEqual(tuple(expected_options), tuple(actual_options))


class TestOption(unittest.TestCase):
    def xtest_ctor_validation_successes(self):
        Option("a", "-a", "All", "STUFF")
        Option("a", "-a", "All", None)
        Option("a", "-a", None, "STUFF")
        Option("a", "-a", None, None)

    def test_ctor_validation_fails_missing_params(self):
        names_switches = [
            ("a", None),
            (None, "-a"),
            (None, None),
            (" ", None),
        ]
        for name_switch in names_switches:
            name = name_switch[0]
            switch = name_switch[1]
            try:
                Option(name, switch, None, None)
                self.fail()
            except ValueError as e:
                self.assertEqual("both 'name' and 'switch' must be provided", e.args[0])

    def test_ctor_validation_fails_invalid_name(self):
        names = [
            " ",
            "a b",
            "a/b",
            "a.b",
        ]
        for name in names:
            try:
                Option(name, "-a", None, None)
                self.fail()
            except ValueError as e:
                msg = "option name should contain no chars illegal for python symbols: '%s'" % name
                self.assertEqual(msg, e.args[0])


class TestCommand(unittest.TestCase):
    def test_chaining_of_options(self):
        options = {
            "l": Option("l", "-l", None, None),
            "a": Option("a", "-a", None, None),
        }
        ls = Command(binary="ls", options=options)

        self.assertEqual(["ls"], ls.argv())
        self.assertEqual(["ls", "-l"], ls.l().argv())
        self.assertEqual(["ls", "-a", "-l"], ls.a().l().argv())

    def test_command_states_are_isolated(self):
        options = {
            "l": Option("l", "-l", None, None),
            "a": Option("a", "-a", None, None),
            "t": Option("t", "-t", None, None),
        }
        ls = Command(binary="ls", options=options)
        ls_a = ls.a()
        ls_al = ls_a.l()
        ls_at = ls_a.t()

        self.assertEqual(["ls"], ls.argv())
        self.assertEqual(["ls", "-a"], ls_a.argv())
        self.assertEqual(["ls", "-a", "-l"], ls_al.argv())
        self.assertEqual(["ls", "-a", "-t"], ls_at.argv())

    def test_command_subclass(self):
        options = {
            "l": Option("l", "-l", None, None),
            "a": Option("a", "-a", None, None),
            "t": Option("t", "-t", None, None),
        }

        class LsCommand(Command):
            def __init__(self, *args, **kwargs):
                kwargs["options"] = options
                Command.init(self, "ls", **kwargs)

            def l(self):
                # We will check that the -l option is processed.
                return self.super_l()

            def a(self):
                # We will check that the -a option is ignored.
                return self

            def l_and_a_and_t(self):
                # We want to invoke the a() method of our parent class
                return self.l().super_a().t()

        ls = LsCommand()
        ls_a = ls.a()
        ls_al = ls_a.l()
        ls_at = ls_a.t()

        self.assertEqual(["ls"], ls.argv())
        self.assertEqual(["ls"], ls_a.argv())
        self.assertEqual(["ls", "-l"], ls_al.argv())
        self.assertEqual(["ls", "-t"], ls_at.argv())
        self.assertEqual(["ls", "-l", "-a", "-t"], ls.l_and_a_and_t().argv())
