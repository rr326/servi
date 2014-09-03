from config import *
from Command import Command
from servi_exceptions import ForceError
import globals as g
from utils import *
from ._commands_utils import  *






def check_errors(force, changed_files, existing_version, new_version):
    if not force and changed_files:
        raise ForceError('The following files from the template were changed'
                         ' unexpectedly: {0}'.format(changed_files))

    if not force and existing_version > new_version:
        raise ForceError('Existing template version ({0}) '
                         '> new version ({1})'.format(existing_version,
                         new_version))


       

class InitCommand(Command):
    def register_command_line(self, sub_parsers):

        parser_init = sub_parsers.add_parser('init', help='Init project')
        parser_init.add_argument('-f', '--force', action='store_true')
        parser_init.add_argument('-q', '--quiet', action='store_true')
        parser_init.set_defaults(command_func=self.run)

    def run(self, args):
        g.quiet = args.quiet

        manifest = create_manifest()
        changed_files = compare_digests(manifest)
        existing_version, new_version = compare_template_versions(manifest)

        check_errors(
            force=args.force, changed_files=changed_files,
            existing_version=existing_version, new_version=new_version)

        qprint('Initializing repository with Servi template version: {0}'.
               format(new_version))
        qprint('Master (destination directory): {0}'.format(MASTER_DIR))

        copy_files(manifest)


command = InitCommand()

