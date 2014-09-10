from command import Command
from commands.utils.manifest import *
from servi_exceptions import *


def error_if_changed(force, changed_files, existing_version, new_version):
    if not force and changed_files:
        raise ForceError(
            'The following files from the template were changed'
            ' unexpectedly:\n  {0}'.format(changed_files))

    if not force and existing_version > new_version:
        raise ForceError('Existing template version ({0}) '
                         '> new version ({1})'
                         .format(existing_version, new_version))


class InitCommand(Command):
    def register_command_line(self, sub_parsers):

        parser_init = sub_parsers.add_parser('init', help='Init project')
        parser_init.add_argument('-f', '--force', action='store_true')
        parser_init.add_argument('-q', '--quiet', action='store_true')
        parser_init.set_defaults(command_func=self.run)

    def run(self, args):
        g.quiet = args.quiet

        m_master = Manifest(MASTER)
        m_template = Manifest(TEMPLATE)

        changed_files = m_master.changed_files(
            m_template, include_deleted=False)

        error_if_changed(
            force=args.force, changed_files=changed_files,
            existing_version=m_template.template_version,
            new_version=m_master.template_version)

        qprint('Master Directory: {0}'
               .format(os.path.abspath(MASTER_DIR)))

        copy_files(m_template, exclude_files=[])


command = InitCommand()
