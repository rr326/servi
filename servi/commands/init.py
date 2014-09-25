from servi.command import Command
from servi.exceptions import *
from servi.utils import *

from servi.manifest import *
from servi.template_mgr import TemplateManager
from servi.config import set_master_dir, load_user_config, servi_file_exists_in


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
        """
        servi init [-f] dir

        if -f
            do it
        else
            if ServiFile exists
                ForceError
            else
                do it

        do it:
            if no directory:
                Make directory
            do_init

        """
        g.quiet = args.quiet
        print('args.dir: {0} {1} '.format(args.dir, os.path.abspath(args.dir)))
        print('cwd: {0}'.format(os.getcwd()))

        def assert_doit():
            if args.force:
                return True
            else:
                if servi_file_exists_in(args.dir):
                    raise ForceError(
                        'ServiFile already exists in: {0}.\n'
                        .format(os.path.abspath(args.dir)))

        assert_doit()
        if not os.path.exists(args.dir):
            os.mkdir(args.dir)
        else:
            if not os.path.isdir(args.dir):
                raise ServiError("Provided directory isn't a directory: {0}"
                    .format(args.dir))

        set_master_dir(set_dir_to=os.path.abspath(args.dir))
        os.chdir(c.MASTER_DIR)

        tmgr = TemplateManager()
        # TODO (?) - Removed 'error_if_changed' - add it back? \
        #  (warn if any files changed)

        qprint('Master Directory: {0}'
               .format(os.path.abspath(c.MASTER_DIR)))

        tmgr.init_master()
        load_user_config()
        return True


command = InitCommand()
