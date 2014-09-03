class ForceError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return (
            '\n***** ERROR *****\n'
            '{0}\n'
            'Use -f / --force to override.\n'
            '\n**Servi Aborting**'.format(self.msg))
