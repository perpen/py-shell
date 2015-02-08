from py_shell.command import Command


class Rsync(Command):
    def __init__(self, *args, **kwargs):
        kwargs["options"] = options
        Command.init(self, "ls", True, **kwargs)

