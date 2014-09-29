from datetime import datetime
import re
import shutil
import os

import yaml

from servi.manifest import Manifest
from servi.exceptions import ServiError, ForceError
from servi.utils import qprint, file_exists, pathfor
import servi.config as c

BACKUP_PREFIX = '_BACKUP_'


class TemplateManager(object):
    def __init__(self, raw_template_playbook=None):
        if re.search('_tmp_', c.TMPL_DIR_SITE):
            print('****** TMPL_DIR_SITE: {0}'.format(c.TMPL_DIR_SITE))
            
        self.m_master = None
        self.m_master_saved = None
        self.m_template = None
        self.master_playbook_exists = ForceError
        self.added_files = set()
        self.changed_files = set()
        self.removed_files = set()
        self.changed_but_ignored_files = set()
        self.mm_added_files = set()
        self.mm_changed_files = set()
        self.mm_removed_files = set()
        self.mm_changed_but_ignored_files = set()
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
        self.added_files, self.changed_files, self.removed_files = \
            Manifest.diff_files(self.m_master, self.m_template)
        self.changed_but_ignored_files = self._ignored_files(
            self.changed_files | self.removed_files)

        # These compare current master to the saved master manifest
        if self.m_master_saved:
            self.mm_added_files, self.mm_changed_files, \
                self.mm_removed_files = \
                Manifest.diff_files(self.m_master, self.m_master_saved)
            self.mm_changed_but_ignored_files = self._ignored_files(
                self.mm_changed_files | self.mm_removed_files)
        else:
            self.mm_added_files, self.mm_changed_files, \
                self.mm_removed_files, self.mm_changed_but_ignored_files = \
                set(), set(), set(), set()

        rm = RoleManager(self.changed_files, self.raw_template_playbook)
        self.roles = rm.roles
        self.possible_roles = rm.possible_roles
        self.modified_possible_roles = rm.modified_possible_roles
        self.role_of_fname = rm.role_of_fname

    def init_master(self):
        self.copy_files(exclude_files=[])

    def update_master(self):
        self.copy_files(exclude_files=self.changed_but_ignored_files)

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

        qprint('backing up: {0}'.format(fname))
        shutil.move(pathfor(fname, c.MASTER), subdir)

    def copy_files(self, exclude_files):
        for normalized_fname, template_hash in \
                self.m_template.manifest["files"].items():

            template_fname = pathfor(normalized_fname, c.TEMPLATE)
            master_fname = pathfor(normalized_fname, c.MASTER)

            # Exclude unchanged files
            if (self.m_master.manifest["files"][normalized_fname] ==
                    template_hash):
                continue

            # Exclude ignored files
            if normalized_fname in exclude_files:
                continue

            # Possibly exclude roles
            # noinspection PyCallingNonCallable
            _cur_role = self.role_of_fname(normalized_fname)
            if (_cur_role and self.master_playbook_exists
                    and _cur_role not in self.roles):
                qprint('Skipping unused role file: {0}'
                       .format(normalized_fname))
                continue

            # Always backup (never overwrite) master
            if file_exists(master_fname):
                self.rename_master_file(normalized_fname, self.timestamp)
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

        # Recreate the master manifest
        m = Manifest(c.MASTER)
        m.save()
        # Then update the template manager based on current (updated) status
        self.update_tmgr()
        return True

    @staticmethod
    def _ignored_files(files):
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
        apache_config/sites_available/THISSITE --> None
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
        roles = set(playbook['roles'])

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

