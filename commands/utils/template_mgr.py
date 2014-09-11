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

        self.changed_but_ignored_files = _ignored_files(self.changed_files | self.removed_files)

        self.timestamp = datetime.utcnow() # used for backups

    def init_master(self):
        _copy_files(self.m_template, exclude_files=[])

    def update_master(self):
        _copy_files(self.m_template, exclude_files=self.changed_but_ignored_files)

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

        qprint('backing up: {0}'.format(fname))
        shutil.move(pathfor(fname, MASTER), backupdir)

def _ignored_files(files):
    """
    Looks in servi_config.yml for a list of ignored files (regex)
    Returns the subset of input files that are matched.
    (Note - looks for config in MASTER. If not found, uses default in TEMPLATE)
    """
    try:
        with open(pathfor(SERVI_CONFIG_YML, MASTER)) as f:
            data = yaml.load(f)
    except FileNotFoundError:
        with open(pathfor(SERVI_CONFIG_YML, TEMPLATE)) as f:
            data = yaml.load(f)

    if "SERVI_IGNORE_FILES" not in data:
        raise ServiError('SERVI_IGNORE_FILES not in {0}'.
                         format(SERVI_CONFIG_YML))

    ignore_list = data["SERVI_IGNORE_FILES"]
    ignore_re_string = '('+'|'.join(ignore_list)+')'
    ignore_re = re.compile(ignore_re_string)

    ignored = {file for file in files if ignore_re.search(file)}

    return ignored


def _copy_files(man, exclude_files):
    """
    man = manifest class for TEMPLATE (must be current)
    exclude_files = optional list of files to ignore

    Copies files from TEMPLATE_DIR to MASTER_DIR
    *Never* overrwrites - will always make a backup if file exists.
    """
    assert man.source == TEMPLATE

    for normalized_fname, template_hash in man.manifest["files"].items():
        if normalized_fname == VERSION_FILE:
            continue  # No need to copy version file (its in servi_data.json)

        template_fname = pathfor(normalized_fname, TEMPLATE)
        master_fname = pathfor(normalized_fname, MASTER)

        master_hash = hash_of_file(master_fname)

        # Exclude unchanged files
        if master_hash == template_hash:
            continue

        # Exclude ignored files
        if normalized_fname in exclude_files:
            continue

        # Always backup (never overwrite) master
        if file_exists(master_fname):
            rename_master_file(master_fname)
            existing = True
        else:
            existing = False

        # Copy template to master
        destdir = os.path.normpath(os.path.dirname(master_fname))
        if destdir:
            # noinspection PyArgumentList
            os.makedirs(destdir, exist_ok=True)
        shutil.copy2(template_fname, master_fname)
        if existing:
            qprint('Updated: {0}'.format(master_fname))
        else:
            qprint('Created: {0}'.format(master_fname))

