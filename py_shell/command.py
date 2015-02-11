import subprocess
import re
from types import MethodType
from pprint import pprint


class CommandUsageError(BaseException):
    def __init__(self, msg):
        BaseException.__init__(self, msg)


class Command(object):
    def __init__(self, binary=None, options=None, pred=None, args=[]):
        """
        When creating a Command object, use one of these two forms:
            Command(binary=BINARY)
                No options given, so BINARY is going to be invoked with option --help,
                and the resulting output is going to be parsed to construct the dict
                of options.

            Command(binary=BINARY, options=OPTIONS)
                OPTIONS should be a dict such as:
                {
                    "o": Option("-o", "Specifies output", "OUTPUT"),
                    "v": Option("-v", "Verbose", None),
                }
        """
        # Implementation detail: This constructor will also be called under other forms
        # (with a 'pred' parameter) when chaining option calls.
        if not pred:
            if not binary:
                raise ValueError("missing parameter 'binary'")
            self.binary = binary
            if options:
                self.options = options
            else:
                usage_out, usage_err = self._capture_output([binary, "--help"])
                usage = usage_out + "\n@@@\n" + usage_err
                #print usage
                self.options = self._parse_usage(usage)
            self.args = []
        else:
            self.binary = pred.binary
            self.options = pred.options
            self.args = args

    @classmethod
    def init(cls, self, binary, **kwargs):
        """Must be called from subclasses constructors."""
        kwargs.update(binary=binary)
        Command.__init__(self, **kwargs)

    def run(self):
        argv = self.process_args(self.argv())
        print "Command.run(): %s" % " ".join(argv)
        return self._capture_output(argv)

    def process_args(self, args):
        return args

    def argv(self):
        "Exposed to help subclasses with unit testing."
        argv = [self.binary]
        argv.extend(self.args)
        return argv

    def _capture_output(self, argv):
        return subprocess.Popen(argv,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE).communicate()

    def __getattr__(self, name):
        if name.startswith("super_"):
            # FIXME - document
            name = re.sub("^super_", "", name)
            if name == "run":
                return super(type(self), self).run
        if name in self.options:
            option = self.options[name]
            return Command._make_method_for_object(option, self)
        else:
            raise ValueError("no such option: %s" % name)

    def __getattr__0(self, name):
        if name in self.options:
            option = self.options[name]
            return Command._make_method_for_object(option, self)
        else:
            raise ValueError("no such option: %s" % name)

    @classmethod
    def _make_method_for_object(cls, option, self):
        def func(self, arg=None):
            new_args = list(self.args)
            new_args.append(option.switch)
            if arg:
                new_args.append(arg)
            return self.__class__(pred=self, args=new_args)

        func.__doc__ = help
        func.__name__ = option.name
        method = MethodType(func, self)
        return method

    def arg(self, arg):
        self.args.append(arg)
        return self

    def pipe(self, other):
        # run myself, capture outputs
        # run other, passing input
        pass

    def raise_missing_param(self, *params):
        msg = "missing params: %s" % ", ".join(params)
        raise CommandUsageError(msg)

    def _parse_usage(self, usage):
        return UsageParser().parse(usage)


class Option:
    def __init__(self, name, switch, help, value):
        if not (name and switch):
            raise ValueError("both 'name' and 'switch' must be provided")
        if not re.match("^\w+$", name):
            # We will be using the option name as a method name
            raise ValueError("option name should contain no chars illegal for python symbols: '%s'" % name)
        self.name = name.strip()
        self.switch = switch.strip()
        self.help = help
        self.value = value

    def __repr__(self):
        return "Option(name: %s, switch: %s, help: %s, value: %s)" % (
            self.name,
            self.switch,
            self.help,
            self.value,
        )


class UsageParser:
    def parse(self, usage):
        """
        Parse usage string to construct a dictionnary with entries of the form:
            <switch w/o dashes>: (<switch with dashes> <help message>, <name of parameter>)

        E.g. for these usage lines
            -o, --output=OUTPUT Specifies output
            -v
        We'll get these entries in the dictionnary:
            "o": Option("-o", "Specifies output", "OUTPUT")
            "output": Option("--output", "Specifies output", "OUTPUT")
            "v": Option("-v", None, None)

        """
        ## Find all the options
        rx = re.compile("^\\s+(-[^\\s,]+)(?:,\\s+(-[^\\s,]+))*(?:\\s+([^-].*))?", re.MULTILINE)
        matches = re.findall(rx, usage)
        #if not matches:
            #raise ValueError("unable to parse usage string")

        options = {}
        for match in matches:  # parse each matching line
            # Get rid of empty tokens, which are a side-effect of my regex
            tokens = [token for token in match if token]

            switches = []  # e.g. ["-o", "--output"]
            value = None  # e.g. "FILE"
            help = None  # e.g. "Output file"

            for token in tokens:
                if token.startswith("-"):
                    # Remove "=VALUE" or [=VALUE]from the end.
                    switch = re.sub("\[?=.*$", "", token)
                    switches.append(switch)
                    if "=" in token:
                        value_index = token.index("=") + 1
                        value = token[value_index:]
                else:
                    help = token

            for switch in switches:
                name = re.sub("^-+", "", switch)
                name = re.sub("-", "_", name)
                options[name] = Option(name, switch, help, value)

        return options
