import subprocess
import os
from logging import debug, info, warning as warn, error

from servi.command import Command
import servi.config as c
from servi.template_mgr import TemplateManager
from servi.utils import pathfor, timeit


"""
IMPORTANT NOTE

Running ansible requires some extra variables which I need to define in TWO
places: Vagrantfile (eg: vars["IS_VAGRANT"] = true) and here.

It's ugly and error prone but I can't find an elegant way to do it
(that doesn't overly complicate the Vagrantfile).
"""


def get_ansible_extra_vars(is_local):
    retval = {
        "REMOTE_DIR": "/var/www/"+c.SITE_SUFFIX,
        "APACHE_LOG_DIR": "/var/log/apache2/" + c.SITE_SUFFIX
    }
    if is_local:
        retval["IS_VAGRANT"] = True
    else:
        retval["IS_VAGRANT"] = False

    return retval


def vars_to_cmd_list(extra_vars):
    retval = []

    if type(extra_vars) is dict:
        for key, val in extra_vars.items():
            retval.append('-e {0}={1}'.format(key, val))
    else:
        for val in extra_vars:
            retval.append('-e' + val)
    return retval

class LansCommand(Command):
    def __init__(self):
        self.special = {"parse_known_args": True}

    def register_command_line(self, sub_parsers):

        parser = sub_parsers.add_parser(
            'lans', help="Local ANSible - "
                         "Run ansbile on your local (vagrant) setup.",
            description="Local ANSible - "
                        "Run ansbile on your local (vagrant) setup."
                        "This is a convenience function that sets "
                        "up the ansible command with the proper vagrant_inventory "
                        "file, and ssh user and password, saving you a lot "
                        "of typing. Any arguments not listed below will be "
                        "passed directly 'ansible-playbook'."
        )

        parser.add_argument(
            '-p', '--project_only', action='store_true', help=
            'Only run the "projectSpecific" role.')

        parser.set_defaults(command_func=self.run)

    def run(self, args, extra_args):
        proj_only = ['-t', 'projectSpecific'] if args.project_only else []

        extra_vars = get_ansible_extra_vars(is_local=True)

        # Relative to ansible_config
        cmd_line = [
            'ansible-playbook', 'playbook.yml', '-i',
            '../.vagrant/provisioners/ansible/vagrant_inventory/vagrant_ansible_inventory',
            ] + proj_only + vars_to_cmd_list(extra_vars) + extra_args

        info('Running local ansible with:\n\tcommand line: {0}\n\tcwd:{1}'
             .format(' '.join(cmd_line),
                os.path.join(c.MASTER_DIR, 'ansible_config')))
        with timeit():
            retval = subprocess.call(
                cmd_line, cwd=os.path.join(c.MASTER_DIR, 'ansible_config'))
        return not retval


command = LansCommand()


"""
* TODO
    * Need to set same env variables as vagrantfile (eg: IS_VAGRANT)
    * Need to get it to read ansible.cfg (maybe just change current directory)
    * Following works:

ansible-playbook -C ansible_config/playbook.yml -i .vagrant/provisioners/ansible/vagrant_inventory/vagrant_ansible_inventory  -e ansible_ssh_user=vagrant -e ansible_ssh_private_key_file=/Users/rrosen/.vagrant.d/insecure_private_key
"""