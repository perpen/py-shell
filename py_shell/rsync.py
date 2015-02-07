from py_shell.command import Command


class Rsync(Command):
    def __init__(self, src, tgt):
        Command.__init__(self, "rsync", parse_usage=True)
        self.src = src
        self.tgt = tgt
