from pprint import pprint
import json
import os
import shutil
from logging import debug, info, warning as warn, error
import subprocess
import json

from servi.command import Command
from servi.manifest import Manifest
from servi.utils import pathfor
import servi.config as c
from servi.semantic import SemanticVersion, SEMANTIC_VERSIONS, PATCH
from servi.exceptions import ServiError
from copy import deepcopy
from pprint import pformat
import json
import sys
from pprint import pformat

class InventoryCommand(Command):
    def __init__(self):
        self.special = {"skip_init": True}
        self.arglist = []
        self.parser = None

    def register_command_line(self, sub_parsers):

        #
        # Note - this is as-defined by ansible:
        # http://docs.ansible.com/developing_inventory.html
        #
        parser = sub_parsers.add_parser(
            'inventory', help='Print ansible inventory to stdout',
            description='Print ansible inventory to stdout.  The data '
                        'for the inventory comes from Servifile_globals.yml.'
                        ' Example: '
                        '"ansible-playbook prod -i \'servi -v0 inventory \' '
                        'playbook.yml"')

        parser.add_argument(
            '--list',  action='store_true',
            help='List all hosts')

        parser.add_argument(
            '--host', type=str,
            help='List specific host')

        parser.add_argument(
            '--debug', action="store_true",
            help="Debug your HOSTS record.")

        parser.set_defaults(command_func=self.run)

        self.parser = parser
        self.arglist = [arg.dest for arg in parser._optionals._actions
                        if arg.dest != 'help' ]

    def run(self, args, extra_args):
        if args.debug:
            retval = do_debug()
        else:
            retval = do_ansible(args)
        return retval


command = InventoryCommand()


def do_ansible(args):
    master_dir = c.find_master_dir(os.getcwd())
    c.set_master_dir(master_dir)

    _, _, combined = c.load_user_config()

    if not 'HOSTS' in combined:
        retval = {}
    elif args.host:
        retval = combined['HOSTS'].get(args.host, {})
    elif args.list:
        retval = combined['HOSTS'] if combined else {}
    else:
        return False

    text = json.dumps(retval, indent=4)+'\n'
    print(text)  # newline
    return text


def do_debug():
    master_dir = c.find_master_dir(os.getcwd())
    c.set_master_dir(master_dir)

    global_config, user_config, combined = c.load_user_config()
    if 'HOSTS' not in combined:
        print('"HOSTS" record not found in your config files. '
              '(case sensitive)')
        return False

    r = True
    hosts = combined["HOSTS"]
    print('Processed HOSTS record:\n{0}\n'.format(pformat({"HOSTS": hosts})))

    if type(hosts) != dict:
        print('"HOSTS" should be a dict / hash. It is currently a: {0}'
               .format(type(hosts)))
        return False

    for host, rec in hosts.items():
        if type(rec) != dict:
            print('Host "{0}" >> Each "host" record should be a dict / hash. '
                  'It is currently a: {1}'.format(host, type(rec)))
            r = False

        elif 'hosts' not in rec:
            print('Host "{0}" >> "hosts" key not found.'.format(host))
            r = False

        elif type(rec['hosts']) != list:
            print('Host "{0}" >> Each "hosts" record should be a list. '
                  'It is currently a: {1}'
                .format(host, type(rec['hosts'])))
            r = False

        if type(rec) is dict:
            if 'vars' not in rec:
                print('Host "{0}" >> "vars" not found (case sensitive).'.format(host))
                r = False

            elif type(rec['vars']) != dict:
                print('Host "{0}" >> Each "vars" record should '
                      'be a dict / hash. '
                      'It is currently a: {1}'
                    .format(host, type(rec['vars'])))
                r = False
    if r:
        print('Debug checks passed.  If it is still not working, '
              'good luck with your debugging! \n'
              'Check the ansible documentation here: '
              'http://docs.ansible.com/developing_inventory.html\n'
              'Or try parsing it with an online yaml parser like: '
              'http://yaml-online-parser.appspot.com/\n'
              '\t(try the python output format)\n')

    return r


"""
Currently debugging usage:
ansible-playbook -l vagrant -i /Users/rrosen/pyvenv/py3.4/bin/servi_inventory -C playbook.yml
ansible-playbook -l vagrant -i `which servi_inventory` -C playbook.yml

"""