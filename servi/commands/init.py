from servi.command import Command, set_master_dir, load_user_config
from servi.manifest import *
from servi.servi_exceptions import *
from servi.template_mgr import TemplateManager
from servi.utils import *


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
        parser_init.add_argument(
            'dir',
            help='Directory to initialize servi with. '
                 'This is usually the root dir of your project. '
                 '"." is a good choice.')
        parser_init.add_argument('-f', '--force', action='store_true')
        parser_init.add_argument('-q', '--quiet', action='store_true')
        parser_init.set_defaults(command_func=self.run)

    def run(self, args):
        g.quiet = args.quiet
        print('args.dir: {0} {1} '.format(args.dir, os.path.abspath(args.dir)))
        print('cwd: {0}'.format(os.getcwd()))

        try:
            os.chdir(args.dir)
            existing_servi = find_master_dir()
        except MasterNotFound:
            pass  # Good
        except FileNotFoundError:
            raise ServiError('Directory not found: {0} '
                .format(os.path.abspath(args.dir)))
        else:
            # Uh oh - there is another one already
            raise ForceError(
                'There is already a servi directory at or '
                'above the directory you provided:\n'
                '\tprovided: {0}\n'
                '\tfound: {1}'
                .format(os.path.abspath(args.dir), existing_servi))

        set_master_dir(set_dir_to=os.path.abspath(args.dir))

        load_user_config()

        tmgr = TemplateManager()

        changed_files = tmgr.changed_files

        error_if_changed(
            force=args.force, changed_files=changed_files,
            existing_version=tmgr.m_template.template_version,
            new_version=tmgr.m_master.template_version)

        qprint('Master Directory: {0}'
               .format(os.path.abspath(c.MASTER_DIR)))

        tmgr.init_master()
        return True


command = InitCommand()
