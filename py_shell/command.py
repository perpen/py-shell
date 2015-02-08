import subprocess
import re
from types import MethodType
from pprint import pprint


class Command:
    def __init__(self, binary=None, options=None, parse_usage=False, pred=None, args=[]):
        if pred:
            self.binary = pred.binary
            self.options = pred.options
            #self._register_options()
            self.args = args
        else:
            #TODO - detect overriden methods?
            #print "self.class:", self.__class__.__name__

            self.binary = binary
            if not (options or parse_usage) or (options and parse_usage):
                raise ValueError("provide constructor with one of: parse_usage, options")
            if parse_usage:
                usage = self._capture_output([binary, "--help"])
                self.options = self._parse_usage(usage)
            else:
                self.options = options
            #self._register_options()
            self.args = []

    def run(self):
        argv = [self.binary]
        argv.extend(self.args)
        print "running: %s" % " ".join(argv)

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

        ##FIXME
        options = {
            "help": options["help"],
            "literal": options["literal"],
        }
        return options

    def _capture_output(self, argv):
        return subprocess.Popen(argv, stdout=subprocess.PIPE).communicate()[0]

    def _register_options(self):
        for switch, actual_and_help_and_value in self.options.items():
            actual_switch, help, value = actual_and_help_and_value
            self._register_option(switch, actual_switch, help, value)

    def _register_option(self, switch, actual_switch, help, value):
        def add_option(self, arg=None):
            print "stating", switch
            if value and not arg:
                raise ValueError("missing parameter for option %s" % switch)
            if arg and not value:
                raise ValueError("option %s does not take parameter, was given: %s" % (actual_switch, arg))
            args = list(self.args)
            args.append(actual_switch)
            if arg:
                args.append(arg)
            #return Command(pred=self, args=args)
            return self.__class__(pred=self, args=args)
        add_option.__doc__ = help
        add_option.__name__ = switch
        method = MethodType(add_option, self)
        print "self.class:", self.__class__.__name__
        print "self.help: ", self.__dict__.get("help")
        if switch not in dir(self):
            setattr(self, add_option.__name__, method)
        else:
            print "\tnot overriding %s" % switch

    def arg(self, arg):
        self.args.append(arg)
        return self

    def run(self):
        print "running ", self.binary, self.args
