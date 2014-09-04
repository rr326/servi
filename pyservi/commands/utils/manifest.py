# noinspection PyProtectedMember
from commands.utils.utils import *
from copy import deepcopy


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
                        self.manifest["files"][fullpath] = 'NONE'
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

    def changed_files(self, orig, normalize_path):
        """
        compares self to orig.manifest
        if normalize_path, it allows you to compare MASTER to TEMPLATE
         manifests
        :returns  (in self not in orig, different in both, in orig not self)
        """
        if normalize_path:
            d0 = normalize_manifest_paths(orig.manifest, orig.source)
            d1 = normalize_manifest_paths(self.manifest, self.source)
        else:
            d0 = orig.manifest
            d1 = self.manifest

        diff = DictDiffer(d1["files"], d0["files"])
        return diff.added(), diff.changed(), diff.removed()


#
# Utilities
#
def normalize_manifest_paths(manifest, source):
    newm = deepcopy(manifest)
    for file, val in manifest["files"].items():
        newf = normalize_path(file, source)
        newm["files"][newf] = val
        del newm["files"][file]
    return newm


def get_template_version(file):
    with open(file) as f:
        data = json.load(f)
    return data["template_version"]


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

