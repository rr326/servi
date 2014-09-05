from commands.utils.utils import *
from commands.utils.semantic import *


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
                template_file = os.path.join(dirpath, file)
                if self.source is MASTER:
                    hashv = hash_of_file(
                        templatepath_to_destpath(template_file))
                else:
                    hashv = hash_of_file(template_file)

                fname = normalize_path(template_file, TEMPLATE)
                self.manifest["files"][fname] = hashv

        self.template_version = self.manifest["template_version"]
        self.manifest["source"] = self.source
        self.manifest["source_dir"] = TEMPLATE_DIR if TEMPLATE else MASTER_DIR

    def load(self):
        with open(self.fname, 'r') as fp:
            self.manifest = json.load(fp)

    def save(self):
        with open(self.fname, 'w') as fp:
            json.dump(self.manifest, fp, indent=4)

    def __eq__(self, other):
        otherval = lambda x: getattr(other, x, None)
        return (self.manifest == otherval('manifest')
                and
                (SemanticVersion(self.template_version) ==
                 SemanticVersion(otherval('template_version')))
                )

    def changed_files(self, orig):
        """
        compares self to orig.manifest
        if normalize_path, it allows you to compare MASTER to TEMPLATE
         manifests
        :returns  files changed (includes deleted)
        """

        diff = DictDiffer(self.manifest["files"], orig.manifest["files"])
        return diff.changed()


#
# Utilities
#


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

