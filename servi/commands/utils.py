from pprint import pprint
import json
import os
from logging import debug, info, warning as warn, error

from servi.command import Command
from servi.manifest import Manifest
from servi.utils import pathfor
import servi.config as c
from servi.semantic import SemanticVersion, SEMANTIC_VERSIONS, PATCH
from servi.exceptions import ServiError
from copy import deepcopy
from pprint import pformat

class UtilsCommand(Command):
    def __init__(self):
        self.special = {"skip_init": True}
        self.arglist=[]

    def register_command_line(self, sub_parsers):

        parser = sub_parsers.add_parser(
            'utils', help='Developer support tools.',
            description='Developer support tools.  Run with the '
                        '-v0 flag to suppress extra printing.  EG: '
                        '"servi -v0 utils --show_servifile_globals"')

        parser.add_argument(
            '-u', '--update_manifest',  action='store_true',
            help='update manifest to template director.'
            '\nUse as a git hook if you are modifying templates.')
        parser.add_argument('--bump', choices=SEMANTIC_VERSIONS,
                                   help='Bump the version')
        parser.add_argument(
            '-s', '--set_ver', type=str,
            help='Set template version to <string>')

        parser.add_argument(
            '-r', '--render_servifiles', action='store_true', help=
            'Render the servifile templates, filling in all values')

        parser.add_argument(
            '-g', '--show_servifile_globals', action='store_true', help=
            'Print the contents of Servifile_globals.yml. '
            'This is good to add to a pre-commit hook.')

        parser.set_defaults(command_func=self.run)

        self.arglist = [arg.dest for arg in parser._optionals._actions
                        if arg.dest != 'help' ]

    def run(self, args, extra_args):
        if sum([1 for key in self.arglist
                if getattr(args, key)]) > 1:
            raise ServiError('Too many arguments. Only 1 flag per run.\n'
                             'args: {0}'.format(vars(args)))


        if args.update_manifest:
            return update_manifest()

        if args.bump:
            return bump(args.bump)

        if args.set_ver:
            return set_ver(args.set_ver)

        if args.render_servifiles:
            return render()

        if args.show_servifile_globals:
            return show_servifile_globals()


def update_manifest():
    """
    returns False/fail if updated. (so you can use as an error code)
    """
    try:
        m_old_manifest = Manifest(c.TEMPLATE, load=True)
    except FileNotFoundError:
        m_old_manifest = None

    m_template_fresh = Manifest(c.TEMPLATE)
    if Manifest.equal_files(m_old_manifest, m_template_fresh):
        debug('Update Manifest: Skipping (Template directory has not changed)')
        return True
    else:
        m_template_fresh.save()
        bump(PATCH)
        debug('Update Manifest: New manifest of the current template '
              'directory saved to: {0}'.format(m_template_fresh.fname))
        return False


def bump(ver_type):
    with open(pathfor(c.VERSION_FILE, c.TEMPLATE), 'r') as fp:
        data = json.load(fp)

    sv = SemanticVersion(data["template_version"])
    sv.bump_ver(ver_type)

    data["template_version"] = str(sv)

    with open(pathfor(c.VERSION_FILE, c.TEMPLATE), 'w') as fp:
        json.dump(data, fp, indent=4)

    info('Updated VERSION_FILE')
    pprint(data)
    return True


def set_ver(version_string):
    sv = SemanticVersion(version_string)

    data = {"template_version": str(sv)}

    with open(pathfor(c.VERSION_FILE, c.TEMPLATE), 'w') as fp:
        json.dump(data, fp, indent=4)

    info('Updated VERSION_FILE to: {0}'.format(data))

    return True

def render():
    global_config, user_config = c.load_user_config()
    combined = deepcopy(global_config)
    combined.update(user_config)

    print('\nGlobal config: \n{0}'.format(pformat(global_config, indent=4)))
    print('\nUser config: \n{0}\n'.format(pformat(user_config, indent=4)))
    print('\nCombined config: \n{0}\n'.format(pformat(combined, indent=4)))

    return True

def show_servifile_globals():
    if not os.path.exists(c.SERVIFILE_GLOBAL_FULL):
        print('{0} not found.'.format(c.SERVIFILE_GLOBAL_FULL))
        return False
    else:
        with open(c.SERVIFILE_GLOBAL_FULL) as fp:
            text = fp.read()
        print(text)


command = UtilsCommand()
