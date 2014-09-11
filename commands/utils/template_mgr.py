from config import *
from commands.utils.manifest import *
from commands.utils.utils import *
from datetime import datetime

BACKUP_PREFIX = '_BACKUP_'


class TemplateManager(object):
    def __init__(self):
        self.m_master = Manifest(MASTER)
        self.m_template = Manifest(TEMPLATE)

        self.added_files, self.changed_files, self.removed_files = \
            self.m_master.diff_files(self.m_template)

        self.changed_but_ignored_files = self._ignored_files(
            self.changed_files | self.removed_files)

        self.timestamp = datetime.utcnow()  # used for backups

    def init_master(self):
        self.copy_files(exclude_files=[])

    def update_master(self):
        self.copy_files(exclude_files=self.changed_but_ignored_files)

    def rename_master_file(self, fname):
        self.rename_master_file_static(fname, self.timestamp)

    @staticmethod
    def rename_master_file_static(fname, timestamp):
        """
        This basically backs up fname (but MOVES it).
        fname is the normalized fname
        Stored in a dirctory: _BACKUP_{UTC_TIMESTAMP}
        """
        backupdir = '{0}_{1}'.format(BACKUP_PREFIX, timestamp.isoformat())
        if not os.path.exists(backupdir):
            os.mkdir(backupdir)
        subdir = os.path.join(backupdir, os.path.dirname(fname))
        if not os.path.exists(subdir):
            os.makedirs(subdir)

        qprint('backing up: {0}'.format(fname))
        shutil.move(pathfor(fname, MASTER), subdir)

    def copy_files(self, exclude_files):
        for normalized_fname, template_hash in \
                self.m_template.manifest["files"].items():

            # No need to copy version file (its in servi_data.json)
            if normalized_fname == VERSION_FILE:
                continue

            template_fname = pathfor(normalized_fname, TEMPLATE)
            master_fname = pathfor(normalized_fname, MASTER)

            # Exclude unchanged files
            if (self.m_master.manifest["files"][normalized_fname] ==
                    template_hash):
                continue

            # Exclude ignored files
            if normalized_fname in exclude_files:
                continue

            # Always backup (never overwrite) master
            if file_exists(master_fname):
                self.rename_master_file(normalized_fname)
                existing = True
            else:
                existing = False

            # Copy template to master
            destdir = os.path.dirname(master_fname)
            if destdir and not os.path.exists(destdir):
                os.makedirs(destdir)
            shutil.copy2(template_fname, master_fname)
            if existing:
                qprint('Updated: {0}'.format(master_fname))
            else:
                qprint('Created: {0}'.format(master_fname))

    @staticmethod
    def _ignored_files(files):
        """
        Sees if any of files are in the ignore regex set by servi_config.yml
        (initialized in config.py)
        """
        ignore_list = SERVI_IGNORE_FILES
        ignore_re_string = '('+'|'.join(ignore_list)+')'
        ignore_re = re.compile(ignore_re_string)

        ignored = {file for file in files if ignore_re.search(file)}

        return ignored


