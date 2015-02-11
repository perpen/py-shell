from py_shell.command import Command


class Rsync(Command):
    def __init__(self, *args, **kwargs):
        Command.init(self, "rsync", **kwargs)
        self.srcs = None
        self.dest = None

    def sources(self, *srcs):
        for src in srcs:
            pass
        self.srcs = srcs
        return self

    def destination(self, dest):
        self.dest = dest
        return self

    def process_args(self, args):
        print "Rsync.run: args:", args
        print self.srcs

        if not self.srcs:
            self.raise_missing_param("sources")
        if not self.dest:
            self.raise_missing_param("destination")

        args.extend(self.srcs)
        args.append(self.dest)

        return args
