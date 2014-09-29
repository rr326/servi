import subprocess
import os

from servi.command import Command, process_and_run_command_line as servi_run
import servi.config as c
from servi.utils import pathfor
from tempfile import TemporaryDirectory
from servi.template_mgr import TemplateManager
import re


class BuildboxCommand(Command):
    def register_command_line(self, sub_parsers):

        parser_init = sub_parsers.add_parser(
            'buildbox', help="Build a vagrant base box based on the  "
            "current template.", description=
            "Build a vagrant base box based on the current template.\n"
            "Then you can run 'servi usebox' to use the box instead of "
            "rebuilding from scratch.\n"
            "Note - this is simply to save time on servi site #2+\n"
            "You can always do 'servi init' and then 'vagrant up', but "
            "that can take a while every time you do a new site."
        )

        parser_init.set_defaults(command_func=self.run)

    def run(self, args):
        box_name, box_path = get_boxname()

        if os.path.exists(box_path):
            print('servi_box for current template already exists: {0}'
                  .format(box_path))
            print('Exiting')
            return True

        if not os.path.exists(c.BOX_DIR):
            os.mkdir(c.BOX_DIR)

        # Delete any old boxes
        existing_boxes = os.listdir(c.BOX_DIR)
        if existing_boxes:
            for f in existing_boxes:
                if re.match('servi_box_[0-9]+_[0-9]+_[0-9]+\.box', f):
                    os.remove(os.path.abspath(os.path.join(c.BOX_DIR, f)))

        with TemporaryDirectory() as tmpdir:
            print('DEBUG buildbox: tmppath: {0}\n'.format(tmpdir))
            print('This will do a "vagrant up" with the current servi '
                  'template.\nIt could take a while...\n\n')

            # Important - everthing is relative to tmpdir as cwd
            os.chdir(tmpdir)
            servi_run('-q init .')

            subprocess.check_call(['vagrant', 'up'])
            subprocess.check_call(['vagrant', 'package',
                                   '--output', box_path])
            subprocess.check_call(['vagrant', 'destroy', '-f'])
            print('servi box created in: {0}'.format(box_path))
            print('To use, run "servi usebox"\n'
                  'or run: "vagrant init {0}"'.format(box_path))
            pass

        return True


command = BuildboxCommand()


def get_boxname():
    ver = TemplateManager().m_template.template_version
    box_name = 'servi_box_{0}_{1}_{2}.box' \
        .format(ver.sv_ar[0], ver.sv_ar[1], ver.sv_ar[2])
    box_path = os.path.abspath(os.path.join(c.BOX_DIR, box_name))

    return box_name, box_path