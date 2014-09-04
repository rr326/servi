from config import *
from command import Command
from utils import *
from commands.utils.utils import *
from commands.utils.manifest import *


def error_if_changed(force, changed_files, existing_version, new_version):
    if not force and changed_files:
        raise ForceError(
            'The following files from the template were changed'
            ' unexpectedly: {0}'.format(changed_files))

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

        m_existing_fresh = Manifest(MASTER)
        m_existing_fresh.create()
        m_template_fresh = Manifest(TEMPLATE)
        m_template_fresh.create()

        _, changed_files, _ = m_existing_fresh.changed_files(
            m_template_fresh, True)

        error_if_changed(force=args.force, changed_files=changed_files,
            existing_version=m_template_fresh.template_version,
            new_version=m_existing_fresh, use_ignore_list=False)

        qprint('Initializing repository with Servi template version: {0}'.
               format(m_template_fresh))
        qprint('Master (destination directory): {0}'.format(MASTER_DIR))

        copy_files(m_template_fresh.manifest, exclude_files=[])


command = InitCommand()

