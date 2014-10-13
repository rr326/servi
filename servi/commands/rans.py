import subprocess
import os
from logging import debug, info, warning as warn, error
import tempfile

from servi.command import Command
import servi.config as c
from servi.template_mgr import TemplateManager
from servi.utils import pathfor, timeit
from servi.exceptions import ServiError
from servi.commands.lans import get_ansible_extra_vars, vars_to_cmd_list
from pprint import pformat


class RansCommand(Command):
    def __init__(self):
        self.special = {"parse_known_args": True}

    def register_command_line(self, sub_parsers):

        parser = sub_parsers.add_parser(
            'rans', help="Remote ANSible - "
                         "Run ansbile on your remote system.",
            description="Remote ANSible - "
                        "Run ansbile on your remote system."
                        "This is a convenience function that sets "
                        "up the ansible command with the proper inventory "
                        "file, and ssh user and password, saving you a lot "
                        "of typing. Any arguments not listed below will be "
                        "passed directly 'ansible-playbook'."
        )

        parser.add_argument(
            '-p', '--project_only', action='store_true', help=
            'Only run the "projectSpecific" role.')

        parser.add_argument(
            'host_alias',
            help='alias of host to run ansible on. '
                 'This is the key part of the HOSTS field in'
                 'Servifile_globals.yml or Servifile.yml ')

        parser.set_defaults(command_func=self.run)

    def run(self, args, extra_args):
        hostdict = c.HOSTS

        if args.host_alias not in hostdict:
            raise ServiError('Given host alias ({0}) not found in '
                             'Servifile_globals.yml or Servifile.yml '
                             'HOSTS: \n{1}'
                             .format(args.host_alias, pformat(c.HOSTS)))

        alias = args.host_alias
        host = hostdict[alias].get('host')
        proj_only = ['-t', 'projectSpecific'] if args.project_only else []
        extra_vars = get_ansible_extra_vars(is_local=False)

        # I use a temporary inventory file (as opposed to a static one like
        # vagrant uses) because that way the Servifile is the one source of
        # truth, and any changes don't require an intermediat step
        with tempfile.NamedTemporaryFile(mode='w+') as fp:
            fp.write('# Servi-created (temporary) inventory file\n')
            fp.write('{alias} ansible_ssh_host={host}\n'.format(alias=alias, host=host))
            fp.file.flush()
            with open(fp.name, 'r') as tmp:
                debug('Temporary inventory file used for ansible-playbook\n'
                      '{0}'.format(tmp.read()))

            # Relative to ansible_config
            cmd_line = ['ansible-playbook', 'playbook.yml',
                        '--inventory-file', fp.name,
                        '--user', c.MAIN_USERNAME,
                        '--private-key', c.MAIN_RSA_KEY_FILE,
                       ] + proj_only \
                         + vars_to_cmd_list(extra_vars) \
                         + extra_args

            info('Running local ansible with:\n\tcommand line: {0}\n\tcwd:{1}'
                 .format(' '.join(cmd_line),
                        os.path.join(c.MASTER_DIR, 'ansible_config')))
            with timeit():
                retval = subprocess.call(
                    cmd_line, cwd=os.path.join(c.MASTER_DIR, 'ansible_config'))

        return not retval


command = RansCommand()


"""
* TODO
    * Need to set same env variables as vagrantfile (eg: IS_VAGRANT)
    * Need to get it to read ansible.cfg (maybe just change current directory)
    * Following works:

ansible-playbook -C ansible_config/playbook.yml -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory  -e ansible_ssh_user=vagrant -e ansible_ssh_private_key_file=/Users/rrosen/.vagrant.d/insecure_private_key
"""