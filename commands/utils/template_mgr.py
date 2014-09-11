from commands.utils.manifest import *
from commands.utils.utils import *


class TemplateManager(object):
    def __init__(self):
        self.m_master = Manifest(MASTER)
        self.m_template = Manifest(TEMPLATE)

        self.added_files, self.changed_files, self.removed_files = \
            self.m_master.diff_files(self.m_template)


        self.changed_but_ignored_files = ignored_files(self.changed_files)

    def init_master(self):
        copy_files(self.m_template, exclude_files=[])

    def update_master(self):
        copy_files(self.m_template, exclude_files=self.changed_but_ignored_files)
