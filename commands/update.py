from command import Command
from commands.utils.manifest import *
from servi_exceptions import *
from commands.utils.template_mgr import *

class UpdateCommand(Command):
    def register_command_line(self, sub_parsers):

        parser_update = sub_parsers.add_parser(
            'update', help='Update project with latest template')
        parser_update.add_argument('-q', '--quiet', action='store_true')

        parser_update.set_defaults(command_func=self.run)

    def run(self, args):
        g.quiet = args.quiet

        tmgr=TemplateManager()

        changed_or_removed_files = tmgr.changed_files | tmgr.removed_files

        changed_but_ignored_files = ignored_files(changed_or_removed_files)

        if len(changed_or_removed_files - changed_but_ignored_files) > 0:
            raise ServiError(
                'The following files were changed in your master and updated '
                'in the template:\n  {0}\n'
                '\nIf you want to reinitialize your templates '
                '(with automatic backup) run "servi init -f"'
                .format(changed_or_removed_files - changed_but_ignored_files))

        if changed_or_removed_files:
            print('\nWarning\n'
                  'The following files from the template were changed'
                  ' unexpectedly and will not be updated: {0}\n'
                  .format(changed_but_ignored_files))

        qprint('Updating repository with Servi template version: {0}'
               .format(tmgr.m_template.template_version))
        qprint('Master (destination directory): {0}'.format(MASTER_DIR))

        tmgr.update_master()

command = UpdateCommand()
