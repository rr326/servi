from command import Command
from commands.utils.manifest import *
from servi_exceptions import *
import subprocess


class DiffCommand(Command):
    def register_command_line(self, sub_parsers):

        parser_init = sub_parsers.add_parser(
            'diff', help="Diff changes betweeen your server "
                         "config and servi's")
        parser_init.set_defaults(command_func=self.run)

    def run(self, args):
        m_master = Manifest(MASTER)
        m_master.create()
        m_template = Manifest(TEMPLATE)
        m_template.create()

        _, changed, removed = m_master.diff_files(m_template)
        ignored = ignored_files(list(changed) + list(removed))

        print('Diff of servi template and existing MASTER dir.')
        print('===============================================')
        print('Template Directory: {0}'.format(os.path.abspath(TEMPLATE_DIR)))
        print('Master Directory:   {0}'.format(os.path.abspath(MASTER_DIR)))
        print()
        print('Changed files: ')
        print('===============')
        if not changed:
            print('(no changed files)')
        else:
            for file in changed:
                print('\t{0} {1}'.format(
                    file, '[ignored]' if file in ignored else ''))
        print()
        print('Removed (Template files not found in Master): ')
        print('==============================================')
        if not removed:
            print('(no removed template files)')
        else:
            print('\t{0} {1}'.format(
                file, '[ignored]' if file in ignored else ''))
        print()
        print('Added (to master and not in template)')
        print('=====================================')
        print('\t(NOT SHOWN)')
        print()
        print('Showing git diff MASTER TEMPLATE\n')
        for file in changed:
            subprocess.call(
                ['git', '--no-pager', 'diff',
                 os.path.abspath(pathfor(file, MASTER)),
                 os.path.abspath(pathfor(file, TEMPLATE))
                 ])


command = DiffCommand()

# TODO - add git difftool setup
# TODO - add command line parameters pass-through
