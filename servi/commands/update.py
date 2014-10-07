from logging import debug, info, warning as warn, error
from servi.command import Command
from servi.exceptions import ServiError
from servi.template_mgr import TemplateManager
import servi.config as c


class UpdateCommand(Command):
    def register_command_line(self, sub_parsers):

        parser_update = sub_parsers.add_parser(
            'update', help='Update project with latest template')

        parser_update.set_defaults(command_func=self.run)

    def run(self, args, extra_args):
        tmgr = TemplateManager()

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
            warn('\nWarning\n'
                 'The following files from the template were changed but\n'
                 'are on your SERVI_IGNORE_FILES list and will not be '
                 'updated:\n'
                 '{0}\n'.format(sorted(changed_but_ignored_files)))

        if tmgr.modified_possible_roles:
            warn('\nWarning\n'
                 'The following lines in your ansible_confg/playbook.yml '
                 'looked like roles that are commented out.\n'
                 'The Template and Master versions differ.\n'
                 '** Because they are commented, they are ignored.**\n'
                 '{0}\n'.format(sorted(tmgr.modified_possible_roles)))

        info('Updating repository with Servi template version: {0}'
               .format(tmgr.m_template.template_version))
        info('Master (destination directory): {0}'.format(c.MASTER_DIR))

        tmgr.update_master()

        return True

command = UpdateCommand()
