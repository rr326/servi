# noinspection PyProtectedMember
from commands.utils.utils import *


class Manifest(object):
    def __init__(self, source):
        assert source in [TEMPLATE, MASTER]
        self.source = source
        self.fname = pathfor(MANIFEST_FILE, source)
        self.manifest = None
        self.template_version = None

    def create(self):
        # create a new manifest
        # use the files in TEMPLATE_DIR as the source list
        self.manifest = {
            "files": {},
            "template_version": get_template_version(
                pathfor(VERSION_FILE, self.source)),
        }

        for (dirpath, dirnames, filenames) in os.walk(TEMPLATE_DIR):
            for file in filenames:
                fullpath = os.path.join(dirpath, file)
                if self.source is MASTER:
                    fullpath = templatepath_to_destpath(fullpath)
                    if not (os.path.isfile(fullpath) and
                            os.access(fullpath, os.R_OK)):
                        continue  # If MASTER doesn't have a template file,
                                  # that's ok
                self.manifest["files"][fullpath] = hash_of_file(fullpath)

        self.template_version = self.manifest["template_version"]

    def load(self):
        with open(self.fname, 'r') as fp:
            self.manifest = json.load(fp)

    def save(self):
        with open(self.fname, 'w') as fp:
            json.dump(self.manifest, fp)

    def __eq__(self, other):
        otherval = lambda x: getattr(other, x, None)
        return (self.manifest == otherval('manifest')
                and
                self.template_version == otherval('template_version')
                )

    def changed_files(self, orig):
        """
        compares self to orig.manifest
        :returns  (in self not in orig, different in both, in orig not self)
        """
        orig_manifest = getattr(orig, 'manifest')
        diff = DictDiffer(self.manifest['files'], orig_manifest['files'])
        return diff.added(), diff.changed(), diff.removed()


def get_template_version(file):
    with open(file) as f:
        data = json.load(f)
    return data["template_version"]


def compare_template_versions(manifest):
    try:
        existing_version = get_template_version(
            templatepath_to_destpath(VERSION_FILE))
    except FileNotFoundError:
        existing_version = ''
    return existing_version, manifest["template_version"]


def compare_digests(manifest):
    # Returns a list of files that are in the template directory but have
    # been changed in the master directory
    warn = []
    for file, sha1 in manifest["files"].items():
        path = templatepath_to_destpath(file)
        if os.path.isfile(path) and os.access(path, os.R_OK):
            if hash_of_file(path) != sha1:
                warn.append(path)
    return warn


# http://stackoverflow.com/a/1165552/1400991
class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = \
            set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self):
        return self.set_current - self.intersect

    def removed(self):
        return self.set_past - self.intersect

    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] !=
                   self.current_dict[o])

    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] ==
                   self.current_dict[o])

