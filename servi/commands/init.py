import os
from logging import debug, info, warning as warn, error

import servi.config as c
from servi.command import Command
from servi.exceptions import ForceError, ServiError

from servi.template_mgr import TemplateManager
from servi.config import set_master_dir, load_user_config, \
    servi_file_exists_in, global_servi_file_exists


class InitCommand(Command):
    def __init__(self):
        self.special = {"skip_init": True}

    def register_command_line(self, sub_parsers):
        parser = sub_parsers.add_parser('init', help='Init project')
        parser.add_argument(
            'dir',
            help='Directory to initialize servi with. '
                 'This is usually the root dir of your project. '
                 '"." is a good choice.')
        parser.add_argument('-f', '--force', action='store_true')
        parser.add_argument('-s', '--skip_servifile_globals', action='store_true')
        parser.set_defaults(command_func=self.run)

    def run(self, args, extra_args):
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
        def assert_doit():
            if args.force:
                return True
            else:
                if servi_file_exists_in(args.dir):
                    raise ForceError(
                        'Servifile already exists in: {0}.\n'
                        .format(os.path.abspath(args.dir)))
                if (not args.skip_servifile_globals and
                    global_servi_file_exists()):
                    raise ForceError(
                        'Servifile_globals already exists in: {0}.\n'
                            .format(c.SERVIFILE_GLOBAL_FULL))

        assert_doit()
        if not os.path.exists(args.dir):
            os.mkdir(args.dir)
        else:
            if not os.path.isdir(args.dir):
                raise ServiError(
                    "Provided directory isn't a directory: {0}"
                    .format(args.dir))

        set_master_dir(set_dir_to=os.path.abspath(args.dir))
        os.chdir(c.MASTER_DIR)

        tmgr = TemplateManager()
        tmgr.init_master(exclude_files=[c.SERVIFILE_GLOBAL]
                         if args.skip_servifile_globals else [])
        load_user_config()
        return True


command = InitCommand()
