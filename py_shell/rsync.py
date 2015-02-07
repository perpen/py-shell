import subprocess
import re
from pprint import pprint


class Command:
    state_classes = {}

    def __init__(self, binary, options=None, parse_usage=False):
        self.binary = binary
        if not (options or parse_usage) or (options and parse_usage):
            raise ValueError("provide constructor with one of: parse_usage, options")
        if parse_usage:
            usage = self._capture_output([binary, "--help"])
            self.options = self._parse_usage(usage)
        else:
            self.options = options

        if binary not in Command.state_classes:
            state_class = Command._create_state_class(self.__class__,
                                                      self.options)
            Command.state_classes[binary] = state_class

    def params(self):
        return Command.state_classes[self.binary](self)

    def run(self, args):
        argv = [self.binary]
        argv.extend(args)
        print "CommandState: running: %s" % " ".join(argv)

    def pipe(self, other):
        # run myself, capture outputs
        # run other, passing input
        pass

    def _parse_usage(self, usage):
        """ Parse usage to construct a dictionnary with entries of the form:
            <switch w/o dashes>: (<switch with dashes> <help message>, <name of parameter>)

        E.g. for these usage lines
            -o, --output=OUTPUT Specifies output
            -v
        We'll get these entries in the dictionnary:
            "o": ("-o", "Specifies output", "OUTPUT")
            "output": ("--output", "Specifies output", "OUTPUT")
            "v": ("-v", None, None)
        """
        ## First find all the options
        rx = re.compile("^\\s+(-[^\\s,]+)(?:,\\s+(-[^\\s,]+))*(?:\\s+([^-].*))?", re.MULTILINE)
        matches = re.findall(rx, usage)
        if not matches:
            raise ValueError("unable to parse usage string")

        options = {}
        for match in matches:  # parse each matching line
            # Get rid of empty tokens, which are a side-effect of my regex
            tokens = [token for token in match if token]

            switches = []  # e.g. ["-o", "--output"]
            actual_switch = None
            value = None  # e.g. "FILE"
            help = None  # e.g. "Output file"

            for token in tokens:
                if token.startswith("-"):
                    # Remove dashes from the beginning, and "=VALUE" from the end.
                    actual_switch = re.sub("=.*$", "", token)
                    switch = re.sub("(^-+|=.*$)", "", token)
                    switches.append(switch)
                    if "=" in token:
                        value_index = token.index("=") + 1
                        value = token[value_index:]
                else:
                    help = token

            for switch in switches:
                options[switch] = (actual_switch, help, value)

        #pprint(options)
        return options

    def _capture_output(self, argv):
        return subprocess.Popen(argv, stdout=subprocess.PIPE).communicate()[0]

    @classmethod
    def _create_state_class(cls, command_class, options):
        state_class = type("%sCommandState" % command_class.__name__, (CommandState,), {})
        Command._register_options(state_class, options)
        return state_class

    @classmethod
    def _register_options(cls, klass, options):
        for switch, actual_and_help_and_value in options.items():
            actual_switch, help, value = actual_and_help_and_value
            Command._register_option(klass, switch, actual_switch, help, value)

    @classmethod
    def _register_option(cls, klass, switch, actual_switch, help, value):
        def add_option(self, arg=None):
            print "stating", switch
            self.args.append(actual_switch)
            if value and not arg:
                raise ValueError("missing parameter for option %s" % switch)
            if arg and not value:
                raise ValueError("option %s does not take parameter, was givent: %s" % (actual_switch, arg))
            if arg:
                self.args.append(arg)
            return self
        add_option.__doc__ = help
        add_option.__name__ = switch
        setattr(klass, add_option.__name__, add_option)


class CommandState(object):
    def __init__(self, command):
        self.command = command
        self.args = []

    def arg(self, arg):
        self.args.append(arg)
        return self

    def run(self):
        self.command.run(self.args)


class Rsync(Command):
    def __init__(self, src, tgt):
        Command.__init__(self, "rsync", parse_usage=True)
        self.src = src
        self.tgt = tgt
