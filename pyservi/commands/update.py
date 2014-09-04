from command import Command
# noinspection PyProtectedMember
from commands.utils.utils import *


class UpdateCommand(Command):
    def register_command_line(self, sub_parsers):

        parser_update = sub_parsers.add_parser(
            'update', help='Update project with latest template')
        parser_update.add_argument('-f', '--force', action='store_true')
        parser_update.add_argument('-q', '--quiet', action='store_true')

        parser_update.set_defaults(command_func=self.run)

    def run(self, args):
        g.quiet = args.quiet

        # manifest = create_manifest()
        # changed_files = compare_digests(manifest)
        # existing_version, new_version = compare_template_versions(manifest)
        #
        # error_if_changed(
        #     force=args.force, changed_files=changed_files,
        #     existing_version=existing_version, new_version=new_version)
        #
        # find_deleted_files()
        #
        # qprint('Updating repository with Servi template version: {0}'.
        #        format(new_version))
        # qprint('Master (destination directory): {0}'.format(MASTER_DIR))
        #
        # copy_files(manifest)

command = UpdateCommand()

## TODO - How to deal with files that were deleted in MASTER_DIR
## (eg: THIS_SITE.conf)