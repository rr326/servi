from logging import debug, info, warning as warn, error
from servi.command import Command
from servi.exceptions import ServiError
from servi.template_mgr import TemplateManager
import servi.config as c
from servi.command import process_and_run_command_line as servi_run


"""
Logic:
    * Error if
        * Master is changed and template is changed (and not ignored)
    * Warning if
        * Ignored file and master and template both changed
          (eg: template Servifile has new content)
        * Possible role changed
          (eg: role in playbook.yml is commented out but still there and
           is changed)
"""


class UpdateCommand(Command):
    def register_command_line(self, sub_parsers):

        parser_update = sub_parsers.add_parser(
            'update', help='Update project with latest template')

        parser_update.set_defaults(command_func=self.run)

    def run(self, args, extra_args):
        t = TemplateManager()
        ignored = TemplateManager.ignored_files


        master_and_tmpl_changed = t.m_mod & t.t_mod
        #if len(changed_or_removed_files - changed_but_ignored_files) > 0:
        if master_and_tmpl_changed - ignored(master_and_tmpl_changed):
            raise ServiError(
                'The following files were changed in your master and updated '
                'in the template:\n'
                '{0}\n\n'
                'If you want to reinitialize your templates '
                '(with automatic backup) run "servi init -f". \n'
                'If you want to copy a specific file, do "servi copy". \n'
                'To see all changes, do "servi diff".'
                .format(master_and_tmpl_changed
                        - ignored(master_and_tmpl_changed)))

        if ignored(master_and_tmpl_changed):
            warn('The following files from the template were changed but\n'
                 'are on your SERVI_IGNORE_FILES list and will not be '
                 'updated:\n'
                 '{0}\n\n'
                 'Try a "servi diff" followed by "servi copy" to manually '
                 'update changed ignored files.\n'
                 .format(sorted(ignored(master_and_tmpl_changed))))

        if t.modified_possible_roles:
            warn('The following lines in your ansible_confg/playbook.yml '
                 'looked like roles that are commented out.\n'
                 'The Template and Master versions differ.\n'
                 '** Because they are commented, they are ignored.**\n'
                 '{0}\n'.format(sorted(t.modified_possible_roles)))

        info('Updating MASTER with Servi template version: {0}'
               .format(t.m_template.template_version))

        t.update_master()

        info('MASTER updated. Showing diff (after update).')
        servi_run("-v2 diff -l")

        return True

command = UpdateCommand()
