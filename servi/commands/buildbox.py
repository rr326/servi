import subprocess
import os

from servi.command import Command, process_and_run_command_line as servi_run
import servi.config as c
from servi.utils import pathfor, timeit
from tempfile import TemporaryDirectory
from servi.template_mgr import TemplateManager
import re
from servi.semantic import SemanticVersion
import argparse
from servi.manifest import get_template_version
from logging import debug, info, warning as warn, error

SKIPPED = 'SKIPPED'


class BuildboxCommand(Command):
    def __init__(self):
        self.special = {"skip_init": True}

    def register_command_line(self, sub_parsers):

        parser = sub_parsers.add_parser(
            'buildbox', help="Build a vagrant base box based on the  "
            "current template.", description=
            "Build a vagrant base box based on the current template.\n"
            "Then you can run 'servi usebox' to use the box instead of "
            "rebuilding from scratch.\n"
            "Note - this is simply to save time on servi site #2+\n"
            "You can always do 'servi init' and then 'vagrant up', but "
            "that can take a while every time you do a new site."
        )

        # for testing
        parser.add_argument('--mock', action='store_true',
                            help=argparse.SUPPRESS)

        parser.set_defaults(command_func=self.run)

    def run(self, args, extra_args):
        box_name, box_path = get_boxname()

        if os.path.exists(box_path):
            warn('servi_box for current template already exists: {0}'
                  .format(box_path))
            warn('Exiting')
            return SKIPPED

        if not os.path.exists(c.BOX_DIR):
            os.mkdir(c.BOX_DIR)

        # Delete any old boxes
        existing_boxes = get_all_boxes()
        if existing_boxes:
            for f in existing_boxes:
                os.remove(os.path.abspath(os.path.join(c.BOX_DIR, f[0])))

        orig_dir = os.getcwd()
        with TemporaryDirectory() as tmpdir:
            debug('buildbox tmppath: {0}\n'.format(tmpdir))
            info('This will do a "vagrant up" with the current servi '
                  'template.\nIt could take a while...\n\n')

            # Important - everthing is relative to tmpdir as cwd
            os.chdir(tmpdir)
            servi_run('-v0 init .')

            # Note - do all vagrant calls with the shell, since
            # servi uses python3 in a venv, and vagrant uses ansible
            # which might be installed globally
            if not args.mock:
                with timeit():
                    subprocess.check_call('vagrant up', shell=True)
                    subprocess.check_call(
                        'vagrant package --output {0}'.format(box_path),shell=True)
                    subprocess.check_call('vagrant destroy -f', shell=True)
            else:
                info('mocking vagrant package with base box: {0}'.format(
                      box_path))
                with open(box_path, 'w') as fp:
                    fp.write('mocked base box')

            info('servi box created in: {0}'.format(box_path))
            info('To use, run "servi usebox"\n'
                  'or run: "vagrant init {0}"'.format(box_path))

        os.chdir(orig_dir)
        return True


command = BuildboxCommand()


def get_boxname():
    ver = SemanticVersion(get_template_version())
    box_name = 'servi_box_{0}_{1}_{2}.box' \
        .format(ver.sv_ar[0], ver.sv_ar[1], ver.sv_ar[2])
    box_path = os.path.abspath(os.path.join(c.BOX_DIR, box_name))

    return box_name, box_path


def get_all_boxes():
    # Returns a SORTED list of all boxes in c.BOX_DIR
    # Sorted by semantic version
    # It is a tuple of [filename, semanticVersion, ...]

    boxes = []
    try:
        existing_boxes = os.listdir(c.BOX_DIR)
    except FileNotFoundError:
        return []

    if existing_boxes:
        boxes = []
        for f in existing_boxes:
            match = re.match('servi_box_([0-9]+_[0-9]+_[0-9]+)\.box', f)
            if match:
                ver = SemanticVersion(match.group(1).replace('_', '.'))
                boxes.append((f, ver))

        boxes.sort(key=lambda tup: tup[1], reverse=True)

    return boxes

# TODO: usebox - check if template > saved box. Fail not -f
# TODO: unit tests