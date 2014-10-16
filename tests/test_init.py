from servi.exceptions import *
from tests.fixtures import *


class TestInit():
    def test_command_line_params(self, tmpdir):
        proj1 = tmpdir.mkdir('proj1')
        assert servi_run('init {0}'.format(proj1))
        with pytest.raises(ForceError):
            assert servi_run('init {0}'.format(proj1))
        assert servi_run('init -f proj1')

        proj2 = tmpdir.mkdir('proj2')
        proj2.chdir()
        with pytest.raises(ForceError):
            assert servi_run('init .')
        assert servi_run('init --skip_servifile_globals .')

        # No directory stated
        with pytest.raises(ServiError):
            assert servi_run('init')

        # Given a file instead of directory should fail
        fname = proj2.ensure('testfile.txt')
        with pytest.raises(ServiError):
            assert servi_run('init --skip_servifile_globals {0}'.format(fname))

    def test_clean(self, clean_master):
        # init on a clean directory should work

        assert servi_run('init .')
        m1 = Manifest(c.MASTER)
        assert len(m1.manifest['files']) > 10

    def test_synced_file_template_dirty(self, synced_file_template_dirty):
        m0 = synced_file_template_dirty["m0"]
        with pytest.raises(ForceError):
            servi_run('init .')

        assert servi_run('init . -f')

        m1 = Manifest(c.MASTER)
        added, changed, removed = Manifest.diff_files(m1, m0)
        assert changed == {'Vagrantfile'}

    def test_synced_file_template_and_master_dirty(
            self, synced_file_template_and_master_dirty):
        m0 = synced_file_template_and_master_dirty["m0"]

        with pytest.raises(ForceError):
            servi_run('init .')

        assert servi_run('init . -f')

        m1 = Manifest(c.MASTER)
        added, changed, removed = Manifest.diff_files(m1, m0)
        assert changed == {'Vagrantfile'}

    def test_template_only_unused_role(self, template_only_unused_role):
        m0 = template_only_unused_role["m0"]

        m1 = Manifest(c.MASTER)
        added, changed, removed = Manifest.diff_files(m1, m0)
        assert added | changed | removed == set()

    def test_master_only(self, master_only):
        m0 = master_only["m0"]
        assert servi_run('init -f .')

        m1 = Manifest(c.MASTER)
        added, changed, removed = Manifest.diff_files(m1, m0)
        assert added | changed | removed == set()

    def test_template_but_ignored(self, template_but_ignored):
        m0 = template_but_ignored["m0"]

        with pytest.raises(ForceError):
            servi_run('init .')

        assert servi_run('init . -f')

        m1 = Manifest(c.MASTER)
        added, changed, removed = Manifest.diff_files(m1, m0)
        assert changed == {'apache_config/sites-available/mysite.conf'}

    def test_dirty_servifile_globals(self, dirty_servifile_globals):
        print('expanduser: {0}'.format(os.path.expanduser('~')))
        with pytest.raises(ForceError):
            assert servi_run('init .')
        assert servi_run('init -f .')
