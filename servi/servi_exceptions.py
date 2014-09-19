class ForceError(Exception):
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return (
            '\n***** ERROR *****\n'
            '{0}\n'
            'Use -f / --force to override.\n'
            '\n**Servi Aborting**'.format(self.msg))


class ServiError(Exception):
    # Expected errrors. Handle gracefully (ie: no stack dump)
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return (
            '\n***** ERROR *****\n'
            '{0}\n'
            '\n**Servi Aborting**'.format(self.msg))
