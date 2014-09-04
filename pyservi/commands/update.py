from command import Command
# noinspection PyProtectedMember
from commands.utils.utils import *
from commands.utils.manifest import *




class UpdateCommand(Command):
    def register_command_line(self, sub_parsers):

        parser_update = sub_parsers.add_parser(
            'update', help='Update project with latest template')
        parser_update.add_argument('-f', '--force', action='store_true')
        parser_update.add_argument('-q', '--quiet', action='store_true')

        parser_update.set_defaults(command_func=self.run)

    def run(self, args):
        g.quiet = args.quiet

        m_existing_fresh = Manifest(MASTER)
        m_existing_fresh.create()
        m_template_fresh = Manifest(TEMPLATE)
        m_template_fresh.create()

        _, changed_files, deleted_files = m_existing_fresh.changed_files(
            m_template_fresh, True)

        changed_files = remove_ignored_files(changed_files)

        if changed_files:
            print('\nWarning\n'
                  'The following files from the template were changed'
                  ' unexpectedly and will not be updated: {0}\n'
                  .format(changed_files))

        qprint('Updating repository with Servi template version: {0}'
               .format(m_template_fresh.template_version))
        qprint('Master (destination directory): {0}'.format(MASTER_DIR))

        copy_files(m_template_fresh.manifest, exclude_files=changed_files)

command = UpdateCommand()

