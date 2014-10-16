from datetime import datetime
import re
import shutil
import os
from logging import debug, info, warning as warn, error
import yaml

from servi.manifest import Manifest
from servi.exceptions import ServiError, ForceError
from servi.utils import file_exists, pathfor
import servi.config as c


BACKUP_PREFIX = '_BACKUP_'


class TemplateManager(object):
    def __init__(self, raw_template_playbook=None):
        self.m_master = None
        self.m_master_saved = None
        self.m_template = None
        self.master_playbook_exists = ForceError
        # t_* - template changed (since master_saved <> tmpl)
        self.t_added = set()
        self.t_changed = set()
        self.t_removed = set()
        self.t_mod = set()
        self.t_mod_but_ignored = set()
        # m_* - master changed (since master <> master_saved)
        self.m_added = set()
        self.m_changed = set()
        self.m_removed = set()
        self.m_mod = set()
        self.m_mod_but_ignored = set()
        self.roles = set()
        self.possible_roles = set()
        self.modified_possible_roles = set()
        self.role_of_fname = None
        self.timestamp = datetime.utcnow()
        self.raw_template_playbook = raw_template_playbook

        self.m_master = Manifest(c.MASTER)
        self.m_template = Manifest(c.TEMPLATE)

        self.update_tmgr()

    def update_tmgr(self):
        try:
            self.m_master_saved = Manifest(c.MASTER, load=True)
        except FileNotFoundError:
            self.m_master_saved = None

        self.master_playbook_exists = file_exists(
            pathfor('ansible_config/playbook.yml', c.MASTER))

        # These compare master to template
        self.t_added, self.t_changed, self.t_removed = \
            Manifest.diff_files(self.m_master, self.m_template)
        self.t_mod = self.t_changed | self.t_removed
        self.t_mod_but_ignored = self.ignored_files(self.t_mod)

        # These compare current master to the saved master manifest
        if self.m_master_saved:
            self.m_added, self.m_changed, \
                self.m_removed = \
                Manifest.diff_files(self.m_master, self.m_master_saved)
            self.m_mod = self.m_changed | self.m_removed
            self.m_mod_but_ignored = self.ignored_files(
                self.m_mod)
        else:
            self.m_added, self.m_changed, \
                self.m_removed, self.m_mod, \
                self.m_mod_but_ignored =  \
                set(), set(), set(), set(), set()

        rm = RoleManager(self.t_changed, self.raw_template_playbook)
        self.roles = rm.roles
        self.possible_roles = rm.possible_roles
        self.modified_possible_roles = rm.modified_possible_roles
        self.role_of_fname = rm.role_of_fname

    def init_master(self, exclude_files=[]):
        self.copy_files(exclude_files=exclude_files)

    def update_master(self):
        self.copy_files(exclude_files=self.t_mod_but_ignored)

    @staticmethod
    def rename_master_file(fname, timestamp):
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

        debug('Backed up: {0}'.format(fname))
        shutil.move(pathfor(fname, c.MASTER), subdir)

    def copy_files(self, exclude_files):
        for fname, template_hash in \
                self.m_template.manifest["files"].items():

            template_fname = pathfor(fname, c.TEMPLATE)
            master_fname = pathfor(fname, c.MASTER)

            # Exclude unchanged files
            if (self.m_master.manifest["files"][fname] ==
                    template_hash):
                continue

            # Exclude ignored files
            if fname in exclude_files:
                continue

            # Possibly exclude roles
            # noinspection PyCallingNonCallable
            _cur_role = self.role_of_fname(fname)
            if (_cur_role and self.master_playbook_exists
                    and _cur_role not in self.roles):
                debug('Skipping unused role file: {0}'
                       .format(fname))
                continue

            # Handle SERVIFILE_GLOBALS differently
            if fname == c.SERVIFILE_GLOBAL:
                master_fname = c.SERVIFILE_GLOBAL_FULL

            # Always backup (never overwrite) master
            if file_exists(master_fname):
                self.rename_master_file(fname, self.timestamp)
                existing = True
            else:
                existing = False

            # Copy template to master
            destdir = os.path.dirname(master_fname)
            if destdir and not os.path.exists(destdir):
                os.makedirs(destdir)
            shutil.copy2(template_fname, master_fname)
            if existing:
                debug('Updated: {0}'.format(master_fname))
            else:
                debug('Created: {0}'.format(master_fname))

        # Recreate the master manifest
        m = Manifest(c.MASTER)
        m.save()
        # Then update the template manager based on current (updated) status
        self.update_tmgr()
        return True

    @staticmethod
    def ignored_files(files):
        """
        Sees if any of files are in the ignore regex set by Servifile.yml
        (initialized in config.py)
        """
        ignore_list = c.SERVI_IGNORE_FILES
        ignore_re_string = '('+'|'.join(ignore_list)+')'
        ignore_re = re.compile(ignore_re_string)

        ignored = {file for file in files if ignore_re.search(file)}

        return ignored


class RoleManager(object):
    def __init__(self, changed_files, raw_template_playbook=None):
        self.roles, self.possible_roles = self._get_master_roles(
            self._get_template_roles(), raw_template_playbook)

        self.modified_possible_roles = self._get_modified_possible_roles(
            changed_files, self.possible_roles)

    @staticmethod
    def role_of_fname(normalized_fname):
        """
        returns a role if normalized_fname looks like a role
        ansible_config/roles/baseUbuntu/* --> baseUbuntu
        apache_config/sites_available/mysite --> None
        """
        match = re.search('ansible_config/roles/([^/]*)(/.+|)',
                          normalized_fname)
        if not match:
            return None
        else:
            return match.group(1)

    @staticmethod
    def _get_template_roles():
        template_dir = os.path.join(c.TMPL_DIR_SITE, 'ansible_config/roles')
        roles = [path for path in
                 os.listdir(template_dir)
                 if os.path.isdir(os.path.join(template_dir, path))]
        return set(roles)

    @staticmethod
    def _get_master_roles(template_roles, test_raw=None):
        if test_raw:
            playbook = yaml.load(test_raw)
            playbook = playbook[0]
            playbook_raw = test_raw
        else:
            try:
                with open(pathfor('ansible_config/playbook.yml', c.MASTER),
                          'r') as fp:
                    playbook = yaml.load(fp)
                    fp.seek(0)
                    playbook = playbook[0]
                    playbook_raw = fp.read()
            except FileNotFoundError:
                return set(), set()

        if 'roles' not in playbook:
            raise ServiError(
                '"roles" not found in {0}'
                .format(pathfor('ansible_config/playbook.yml', c.MASTER)))

        # Note - a role can also have form of {'role':xx, tags:[yy]}
        roles = {role for role in playbook['roles'] if type(role) is str}
        roles |= {role['role']
                  for role in playbook['roles'] if type(role) is dict}

        # also find 'possible' roles - any template role that is commented out
        possible_roles = set()
        for t_role in template_roles:
            if re.search('^.*#.*{0}\s'.format(t_role), playbook_raw,
                         flags=re.IGNORECASE | re.MULTILINE):
                possible_roles.add(t_role)
        return roles, possible_roles

    @staticmethod
    def _get_modified_possible_roles(changed_files, possible_roles):
        retval = set()
        for fname in changed_files:
            role = RoleManager.role_of_fname(fname)
            if role in possible_roles:
                retval |= {role}
        return retval


