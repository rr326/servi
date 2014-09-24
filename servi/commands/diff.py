import subprocess

from servi.command import Command
from servi.manifest import *
import servi.config as c
from servi.template_mgr import TemplateManager
from servi.utils import pathfor


class DiffCommand(Command):
    def register_command_line(self, sub_parsers):

        parser_init = sub_parsers.add_parser(
            'diff', help="Diff changes betweeen your server "
                         "config and servi's. "
                         "Note - set the DIFFTOOL parameter in {0}"
                         .format(c.SERVIFILE))

        parser_init.add_argument(
            '--difftool', action='store', help=
            'Enter a difftool to use: "difftool master_file template_file" '
            '(surround in quotes)')

        parser_init.set_defaults(command_func=self.run)

    def run(self, args):
        tmgr = TemplateManager()

        changed = tmgr.changed_files
        removed = tmgr.removed_files
        ignored = tmgr.changed_but_ignored_files

        print('Diff of servi template and existing MASTER dir.')
        print('===============================================')
        print('Template Directory: {0}'.format(
            os.path.abspath(c.TMPL_DIR_SITE)))
        print('Master Directory:   {0}'.format(os.path.abspath(c.MASTER_DIR)))
        print()
        print('Changed files:')
        print('===============')
        if not changed:
            print('(no changed files)')
        else:
            for file in sorted(list(changed)):
                print('\t{0} {1}'.format(
                    file, '[on "ignore" list]' if file in ignored else ''))
        print()
        print('Removed (Template files not found in Master):')
        print('=============================================')
        if not removed:
            print('(no removed template files)')
        else:
            for file in sorted(list(removed)):
                print('\t{0} {1}'.format(
                    file, '[on "ignore" list]' if file in ignored else ''))
        print()
        print('Added (to master and not in template):')
        print('======================================')
        print('\t(NOT SHOWN)')
        print()
        print('Showing git diff MASTER TEMPLATE\n')
        for file in changed:
            subprocess.call(
                '{command} {path1} {path2}'.format(
                command=args.difftool if args.difftool else c.DIFFTOOL,
                path1=os.path.abspath(pathfor(file, c.MASTER)),
                path2=os.path.abspath(pathfor(file, c.TEMPLATE))
                ), shell=True)
        return True


command = DiffCommand()

# TODO - add command line parameters pass-through
