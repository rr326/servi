from pprint import pprint
import json
from logging import debug, info, warning as warn, error

from servi.command import Command
from servi.manifest import Manifest
from servi.utils import pathfor
import servi.config as c
from servi.semantic import SemanticVersion, SEMANTIC_VERSIONS, PATCH


class ZZCommand(Command):
    def __init__(self):
        self.special = {"skip_init": True}

    def register_command_line(self, sub_parsers):

        parser_update = sub_parsers.add_parser(
            'zz', help="Developer functions for maintaining servi. "
                       "(you shouldn't need this)")
        parser_update.add_argument(
            '--update_manifest',  action='store_true',
            help='update manifest to template director.'
            '\nUse as a git hook if you are modifying templates.')
        parser_update.add_argument('--bump', choices=SEMANTIC_VERSIONS,
                                   help='Bump the version')
        parser_update.add_argument(
            '--set_ver', type=str,
            help='Set template version to <string>')

        parser_update.set_defaults(command_func=self.run)

    def run(self, args, extra_args):
        _vals = [getattr(args, param)
                 for param in ['update_manifest', 'bump']]
        num_params = sum([1 for v in _vals if v])

        if num_params > 1:
            raise Exception('Too many args sent to zz. \n'
                            'Only do one command at a time.\n'
                            'args: {0}'.format(vars(args)))
        if args.update_manifest:
            return update_manifest()

        if args.bump:
            return bump(args.bump)

        if args.set_ver:
            return set_ver(args.set_ver)


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

command = ZZCommand()
