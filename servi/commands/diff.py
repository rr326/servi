import subprocess
import os
from logging import debug, info, warning as warn, error

from servi.command import Command
import servi.config as c
from servi.template_mgr import TemplateManager
from servi.utils import pathfor


class DiffCommand(Command):
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

        parser.set_defaults(command_func=self.run)

    def run(self, args, extra_args):
        tmgr = TemplateManager()

        changed = tmgr.changed_files
        removed = tmgr.removed_files
        ignored = tmgr.changed_but_ignored_files

        info('Diff of servi template and existing MASTER dir.')
        info('===============================================')
        info('Template Directory: {0}'.format(
            os.path.abspath(c.TMPL_DIR_SITE)))
        info('Master Directory:   {0}\n'.format(os.path.abspath(c.MASTER_DIR)))
        info('Changed files:')
        info('===============')
        if not changed:
            info('(no changed files)')
        else:
            for file in sorted(list(changed)):
                info('\t{0} {1}'.format(
                    file, '[on "ignore" list]' if file in ignored else ''))
        info('\nRemoved (Template files not found in Master):')
        info('=============================================')
        if not removed:
            info('(no removed template files)')
        else:
            for file in sorted(list(removed)):
                info('\t{0} {1}'.format(
                    file, '[on "ignore" list]' if file in ignored else ''))
        info('\nAdded (to master and not in template):')
        info('======================================')
        info('\t(NOT SHOWN)')
        info('\nShowing git diff MASTER TEMPLATE\n')
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
