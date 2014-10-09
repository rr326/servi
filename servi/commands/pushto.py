import subprocess
import os
from logging import debug, info, warning as warn, error
import tempfile

from servi.command import Command
import servi.config as c
from servi.template_mgr import TemplateManager
from servi.utils import pathfor
from servi.exceptions import ServiError
from servi.commands.lans import get_ansible_extra_vars, vars_to_cmd_list
from pprint import pformat


class PushtoCommand(Command):
    def register_command_line(self, sub_parsers):

        parser = sub_parsers.add_parser(
            'pushto', help="push source to remote location",
            description="Push your code to your remote server. This copies "
                        "your apache_config directory up to REMOTE and mirrors"
                        "your source (or other) directory up to REMOTE. "
                        "Note - rsync must be installed on your PATH."
        )

        parser.add_argument(
            '-d', '--dir',
            help='Optional directory to use as source. If absent, will'
                 'use LOCAL_DIR from Servifile.yml')

        parser.add_argument(
            'host_alias',
            help='alias of host.'
                 'This is the "alias" part of the REMOTE_HOSTS field in'
                 'Servifile.yml ')

        parser.set_defaults(command_func=self.run)

    def run(self, args, extra_args):
        hostdict = {rec.get('alias') : rec for rec in c.REMOTE_HOSTS }
        if args.host_alias not in hostdict:
            raise ServiError('Given host alias ({0}) not found in '
                             'Servifile.yml REMOTE_HOSTS: \n{1}'
                .format(args.host_alias, pformat(c.REMOTE_HOSTS)))

        alias = args.host_alias
        host = hostdict[alias].get('host')

        ssh_cmd = '"ssh -l {0} -i {1}"'.format(c.MAIN_USERNAME,
                                             c.MAIN_RSA_KEY_FILE)

        dest_base = '{0}@{1}'.format(c.MAIN_USERNAME, host)

        default_cmd = ['rsync', '--dry_run' '-izhav', '--stats',
                       '--exlude=".DS_Store"', '--recursive', '-e', ssh_cmd,
                       ]
        print(ssh_cmd,'\n',dest_base,'\n', default_cmd)
        # retval = subprocess.call(
        #     cmd_line, cwd=os.path.join(c.MASTER_DIR, 'ansible_config'))

        return True


command = PushtoCommand()

