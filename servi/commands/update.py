from servi.command import Command
from servi.manifest import *
from servi.servi_exceptions import *
from servi.template_mgr import TemplateManager
from servi.utils import *


class UpdateCommand(Command):
    def register_command_line(self, sub_parsers):

        parser_update = sub_parsers.add_parser(
            'update', help='Update project with latest template')
        parser_update.add_argument('-q', '--quiet', action='store_true')

        parser_update.set_defaults(command_func=self.run)

    def run(self, args):
        g.quiet = args.quiet

        tmgr = TemplateManager()
        if not tmgr.m_master_saved:
            raise ServiError('No saved manifest in master directory.\n'
                             'Run "servi init" first.')

        changed_or_removed_files = (tmgr.mm_changed_files |
                                    tmgr.mm_removed_files)

        changed_but_ignored_files = tmgr.mm_changed_but_ignored_files

        if len(changed_or_removed_files - changed_but_ignored_files) > 0:
            raise ServiError(
                'The following files were changed in your master and updated '
                'in the template:\n'
                '{0}\n\n'
                'If you want to reinitialize your templates '
                '(with automatic backup) run "servi init -f"'
                .format(changed_or_removed_files - changed_but_ignored_files))

        if changed_but_ignored_files:
            print('\nWarning\n'
                  'The following files from the template were changed but\n'
                  'are on your SERVI_IGNORE_FILES list and will not be '
                  'updated:\n'
                  '{0}\n'.format(sorted(changed_but_ignored_files)))

        if tmgr.modified_possible_roles:
            print('\nWarning\n'
                  'The following lines in your ansible_confg/playbook.yml '
                  'looked like roles that are commented out.\n'
                  'The Template and Master versions differ.\n'
                  '** Because they are commented, they are ignored.**\n'
                  '{0}\n'.format(sorted(tmgr.modified_possible_roles)))

        qprint('Updating repository with Servi template version: {0}'
               .format(tmgr.m_template.template_version))
        qprint('Master (destination directory): {0}'.format(c.MASTER_DIR))

        tmgr.update_master()

        return True

command = UpdateCommand()
