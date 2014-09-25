import json
import os

from servi.semantic import SemanticVersion
from servi.utils import hash_of_file, templatepath_to_destpath, pathfor, \
    normalize_path
import servi.config as c


class Manifest(object):
    def __init__(self, source, load=False):
        assert source in [c.TEMPLATE, c.MASTER]
        self.source = source
        self.fname = pathfor(c.MANIFEST_FILE, source)
        self.manifest = None
        self.template_version = None
        if load:
            self._load()
        else:
            self._create()

    def _create(self):
        # create a new manifest
        # use the files in TMPL_DIR_SITE as the source list
        self.template_version = SemanticVersion(get_template_version())

        self.manifest = {
            "files": {},
            "template_version": str(self.template_version),
        }

        for (dirpath, dirnames, filenames) in os.walk(c.TMPL_DIR_SITE):
            for file in filenames:
                # Keep the version file and manifest files out of the manifest
                if file == c.VERSION_FILE or file == c.MANIFEST_FILE:
                    continue

                template_file = os.path.join(dirpath, file)
                if self.source is c.MASTER:
                    hashv = hash_of_file(
                        templatepath_to_destpath(template_file))
                else:
                    hashv = hash_of_file(template_file)

                fname = normalize_path(template_file, c.TEMPLATE)
                self.manifest["files"][fname] = hashv

    def _load(self):
        with open(self.fname, 'r') as fp:
            self.manifest = json.load(fp)
        self.template_version = SemanticVersion(
            self.manifest["template_version"])

    def save(self):
        assert c.MANIFEST_FILE not in self.manifest["files"]

        with open(self.fname, 'w') as fp:
            json.dump(self.manifest, fp, indent=4, sort_keys=True)

    @staticmethod
    def equal_versions(m1, m2):
        return (SemanticVersion(m1.manifest["template_version"]) ==
                SemanticVersion(m2.manifest["template_version"]))

    @staticmethod
    def equal_files(m1, m2):
        if not m1 or not m2:
            return False

        diff = DictDiffer(m1.manifest["files"], m2.manifest["files"])
        return set() == diff.added() | diff.changed() | diff.removed()

    def __eq__(self, other):
        return (Manifest.equal_versions(self, other) and
                Manifest.equal_files(self, other))

    @staticmethod
    def diff_files(m1, m0):
        mod_m0 = {k: v for k, v in m0.manifest["files"].items()
                  if v != c.MISSING_HASH}

        mod_m1 = {k: v for k, v in m1.manifest["files"].items()
                  if v != c.MISSING_HASH}

        diff = DictDiffer(mod_m1, mod_m0)
        return diff.added(), diff.changed(), diff.removed()


#
# Utilities
#


def get_template_version():
    with open(pathfor(c.VERSION_FILE, c.TEMPLATE)) as f:
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

    # def unchanged(self):
    #     return set(o for o in self.intersect if self.past_dict[o] ==
    #                self.current_dict[o])

