from py_shell.command import Command


class Rsync(Command):
    def __init__(self, *args, **kwargs):
        Command.init(self, "rsync", **kwargs)

    def sources(self, *sources):
        for source in sources:
            pass
        self.sources = sources
        return self

    def destination(self, dest):
        self.dest = dest
        return self

    def run(self):
        self.super_run()
