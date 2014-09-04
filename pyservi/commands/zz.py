from command import Command
from commands.utils.utils import *
from commands.utils.manifest import *

class ZZCommand(Command):
    def register_command_line(self, sub_parsers):

        parser_update = sub_parsers.add_parser(
            'zz', help="Developer functions for maintaining servi. "
                       "(you shouldn't need this)")
        parser_update.add_argument('--save_manifest',  action='store_true',
                                   help='save manifest to template directory')

        parser_update.set_defaults(command_func=self.run)

    def run(self, args):
        if args.save_manifest:
            save_manifest()


def save_manifest():
    m_template_fresh = Manifest(TEMPLATE)
    m_template_fresh.create()
    m_template_fresh.save()
    print('New manifest of the current template directory saved to: {0}'
          .format(m_template_fresh.fname))


command = ZZCommand()
