import subprocess
import os
from logging import debug, info, warning as warn, error
import tempfile

from servi.command import Command
import servi.config as c
from servi.template_mgr import TemplateManager
from servi.utils import pathfor, reset_cwd
from servi.exceptions import ServiError
from servi.commands.lans import get_ansible_extra_vars, vars_to_cmd_list
from pprint import pformat


def addslash(text):
    # Adds a trailing slash for rsync to use source dir contents
    retval = text if text[-1] == '/' else text+'/'
    return retval


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
                 'use LOCAL_DIR from Servifile.yml.  If relative, must '
                 'be relative to location of Servifile.yml')

        parser.add_argument(
            '-n', '--dry_run', action='store_true',
            help='Perform a trial run with no changes made')

        parser.add_argument(
            '--print_only', action='store_true',
            help='Only print out the rsync command line, but do not execute')

        parser.add_argument(
            'host_alias',
            help='alias of host.'
                 'This is the key part of the HOSTS field in'
                 'Servifile_globals.yml or Servifile.yml ')

        parser.set_defaults(command_func=self.run)


    @staticmethod
    def do_rsync(*args, print_only=False):
        cmd = []
        for arg in args:
            cmd.extend(arg)

        info('rsync command line: {0}\n'.format(' '.join(cmd)))
        if not print_only:
            retval = subprocess.call(' '.join(cmd), shell=True )
        else:
            retval = False

        if retval:
            raise ServiError('Rsync failed. Error code: {0}\n'
                             'rsync cmd: {1}'.format(retval, ' '.join(cmd)))
        return retval

    def run(self, args, extra_args):
        hostdict = c.HOSTS
        if args.host_alias not in hostdict:
            raise ServiError('Given host alias ({0}) not found in '
                             'Servifile.yml HOSTS: \n{1}'
                .format(args.host_alias, pformat(c.HOSTS)))

        if args.dir:
            src_dir = args.dir
        else:
            src_dir = pathfor(c.LOCAL_DIR, c.MASTER)

        alias = args.host_alias
        host = hostdict[alias].get('host')

        ssh_cmd = '"ssh -q -l {0} -i {1}"'.format(c.MAIN_USERNAME,
                                             c.MAIN_RSA_KEY_FILE)

        dest_base = '{1}'.format(c.MAIN_USERNAME, host)

        # -O - problem setting dir times 
        # --no-perms - similar
        default_cmd = ['rsync', '-izhav', '-O', '--no-perms', '--stats',
                       '--exclude=".DS_Store"', '--recursive', '-e', ssh_cmd]

        if args.dry_run:
            default_cmd += ['--dry-run']

        apache_cmd = [
            addslash(pathfor('apache_config/sites-available/', c.MASTER)),
            dest_base+':'+'/etc/apache2/sites-available'
        ]

        src_cmd = [
            addslash(src_dir),
            dest_base + ':' + '/var/www/'+c.SITE_SUFFIX
        ]

        with reset_cwd():
            os.chdir(c.MASTER_DIR)
            self.do_rsync(default_cmd, apache_cmd, print_only=args.print_only)
            self.do_rsync(default_cmd, src_cmd, print_only=args.print_only)

        return True


command = PushtoCommand()

