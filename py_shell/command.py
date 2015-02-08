import subprocess
import re
from types import MethodType
from pprint import pprint


class Command(object):
    @classmethod
    def init(cls, self, binary, parse_usage, **kwargs):
        kwargs.update(binary=binary, parse_usage=parse_usage)
        Command.__init__(self, **kwargs)

    def __init__(self, binary=None, options=None, parse_usage=False, pred=None, args=[]):
        if pred:
            self.binary = pred.binary
            self.options = pred.options
            self.args = args
            print "args:", args
        else:
            self.binary = binary
            if not (options or parse_usage) or (options and parse_usage):
                raise ValueError("provide constructor with one of: parse_usage, options")
            if parse_usage:
                usage = self._capture_output([binary, "--help"])
                self.options = self._parse_usage(usage)
            else:
                self.options = options
            self.args = []


    def _argv(self):
        argv = [self.binary]
        argv.extend(self.args)
        return argv

    def run(self):
        argv = self._argv(self)
        print "running: %s" % " ".join(argv)

    def _capture_output(self, argv):
        return subprocess.Popen(argv, stdout=subprocess.PIPE).communicate()[0]

    def _pass(self, name, arg=None):
        return super(type(self), self).__getattr__(name)(arg)

    def __getattr__(self, name):
        if name in self.options:
            option = self.options[name]
            print "handling option %s" % name
            def f(self, arg=None):
                print "processing option %s" % name
                new_args = list(self.args)
                new_args.append(option.switch)
                if arg:
                    new_args.append(arg)
                return self.__class__(pred=self, args=new_args)
            f.__doc__ = help
            f.__name__ = name
            method = MethodType(f, self)
            return method
        else:
            print "no option: %s" % name

    def _register_option(self, switch, actual_switch, help, value):
        def handle_option(self, arg=None):
            print "stating", switch
            if value and not arg:
                raise ValueError("missing parameter for option %s" % switch)
            if arg and not value:
                raise ValueError("option %s does not take parameter, was given: %s" % (actual_switch, arg))
            args = list(self.args)
            args.append(actual_switch)
            if arg:
                args.append(arg)
            return self.__class__(pred=self, args=args)
        handle_option.__doc__ = help
        handle_option.__name__ = switch
        method = MethodType(handle_option, self)
        if switch not in dir(self):
            setattr(self, handle_option.__name__, method)
        else:
            print "\tnot overriding %s" % switch

    def arg(self, arg):
        self.args.append(arg)
        return self

    def run(self):
        print "running ", self.binary, self.args

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
            value = None  # e.g. "FILE"
            help = None  # e.g. "Output file"

            for token in tokens:
                if token.startswith("-"):
                    # Remove dashes from the beginning, and "=VALUE" from the end.
                    #actual_switch = re.sub("=.*$", "", token)
                    #name = re.sub("(^-+|=.*$)", "", token)
                    switch = re.sub("=.*$", "", token)
                    switches.append(switch)
                    if "=" in token:
                        value_index = token.index("=") + 1
                        value = token[value_index:]
                else:
                    help = token

            for switch in switches:
                name = re.sub("^-+", "", switch)
                options[name] = Option(name, switch, help, value)

        ##FIXME
        #options = {
            #"help": options["help"],
            #"literal": options["literal"],
        #}
        #pprint(options)
        return options


class Option:
    def __init__(self, name, switch, help, value):
        self.name = name
        self.switch = switch
        self.help = help
        self.value = value

    def __repr__(self):
        return "Option(name: %s, switch: %s, help: ..., value: %s)" % (
            self.name,
            self.switch,
            self.value,
        )
