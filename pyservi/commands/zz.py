from command import Command
from commands.utils.manifest import *
from pprint import pprint


class ZZCommand(Command):
    def register_command_line(self, sub_parsers):

        parser_update = sub_parsers.add_parser(
            'zz', help="Developer functions for maintaining servi. "
                       "(you shouldn't need this)")
        parser_update.add_argument('--save_manifest',  action='store_true',
                                   help='save manifest to template directory')
        parser_update.add_argument('--bump', choices=SEMANTIC_VERSIONS,
                                   help='Bump the version')
        parser_update.set_defaults(command_func=self.run)

    def run(self, args):
        if args.save_manifest:
            save_manifest()

        if args.bump:
            bump(args.bump)


def save_manifest():
    m_template_fresh = Manifest(TEMPLATE)
    m_template_fresh.create()
    m_template_fresh.save()
    print('New manifest of the current template directory saved to: {0}'
          .format(m_template_fresh.fname))


def bump(ver_type):
    with open(pathfor(VERSION_FILE, TEMPLATE), 'r') as fp:
        data = json.load(fp)

    sv = SemanticVersion(data["template_version"])
    sv.bump_ver(ver_type)

    data["template_version"] = str(sv)

    with open(pathfor(VERSION_FILE, TEMPLATE), 'w') as fp:
        json.dump(data, fp, indent=4)

    print('Updated VERSION_FILE')
    pprint(data)


command = ZZCommand()
