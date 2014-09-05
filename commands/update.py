from command import Command
from commands.utils.manifest import *
from servi_exceptions import *


class UpdateCommand(Command):
    def register_command_line(self, sub_parsers):

        parser_update = sub_parsers.add_parser(
            'update', help='Update project with latest template')
        parser_update.add_argument('-q', '--quiet', action='store_true')

        parser_update.set_defaults(command_func=self.run)

    def run(self, args):
        g.quiet = args.quiet

        m_existing_fresh = Manifest(MASTER)
        m_existing_fresh.create()
        m_template_fresh = Manifest(TEMPLATE)
        m_template_fresh.create()

        changed_files = m_existing_fresh.changed_files(
            m_template_fresh, include_deleted=True)

        changed_but_ignored_files = ignored_files(changed_files)

        if len(changed_files - changed_but_ignored_files) > 0:
            raise ServiError(
                'The following files were changed in your master and updated '
                'in the template:\n  {0}\n'
                '\nIf you want to reinitialize your templates '
                '(with automatic backup) run "servi init -f"'
                .format(changed_files - changed_but_ignored_files))

        if changed_files:
            print('\nWarning\n'
                  'The following files from the template were changed'
                  ' unexpectedly and will not be updated: {0}\n'
                  .format(changed_but_ignored_files))

        qprint('Updating repository with Servi template version: {0}'
               .format(m_template_fresh.template_version))
        qprint('Master (destination directory): {0}'.format(MASTER_DIR))

        copy_files(m_template_fresh, exclude_files=changed_but_ignored_files)

command = UpdateCommand()
