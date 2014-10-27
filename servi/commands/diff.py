import subprocess
import os

from servi.command import Command
import servi.config as c
from servi.template_mgr import TemplateManager
from servi.utils import pathfor


class DiffCommand(Command):
    def __init__(self):
        super().__init__()
        self.tmgr = None

    def register_command_line(self, sub_parsers):

        parser = sub_parsers.add_parser(
            'diff', help="Diff changes betweeen your server "
                         "config and servi's. "
                         "Note - set the DIFFTOOL parameter in {0}"
                         .format(c.SERVIFILE))

        parser.add_argument(
            '--difftool', action='store', help=
            'Enter a difftool to use: "difftool master_file template_file" '
            '(surround in quotes)')

        parser.add_argument(
            '-l', '--list_only', action='store_true', help=
            'Only list changes')

        parser.set_defaults(command_func=self.run)

    def run(self, args, extra_args):
        self.tmgr = TemplateManager()

        self.list_changes()

        if not args.list_only:
            self.detailed_diff(args.difftool)

        return True

    def list_changes(self):
        changed = self.tmgr.t_changed
        removed = self.tmgr.t_removed
        ignored = self.tmgr.t_mod_but_ignored

        print('\nDiff of servi template and existing MASTER dir.')
        print('===============================================')
        print('Template Directory: {0}'.format(
            os.path.abspath(c.TMPL_DIR_SITE)))
        print('Master Directory:   {0}\n'
              .format(os.path.abspath(c.MASTER_DIR)))
        print('Changed files:')
        print('===============')
        if not changed:
            print('(no changed files)')
        else:
            for file in sorted(list(changed)):
                print('\t{0} {1}'.format(
                    file, '[on "ignore" list]' if file in ignored else ''))
        print('\nRemoved (Template files not found in Master):')
        print('=============================================')
        if not removed:
            print('(no removed template files)')
        else:
            for file in sorted(list(removed)):
                print('\t{0} {1}'.format(
                    file, '[on "ignore" list]' if file in ignored else ''))
        print('\nAdded (to master and not in template):')
        print('======================================')
        print('\t(NOT SHOWN)')

    def detailed_diff(self, difftool):
        for file in self.tmgr.t_changed:
            subprocess.call(
                '{command} {templ} {master}'.format(
                    command=difftool if difftool else c.DIFFTOOL,
                    master=os.path.abspath(pathfor(file, c.MASTER)),
                    templ=os.path.abspath(pathfor(file, c.TEMPLATE))
                ), shell=True)
        

command = DiffCommand()
