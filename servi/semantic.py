from itertools import zip_longest

# Simple semantic versioning (1.2.13) tools
MAJOR = 'major'
MINOR = 'minor'
PATCH = 'patch'
SEMANTIC_VERSIONS = [MAJOR, MINOR, PATCH]


class SemanticVersion(object):
    mult = [10**8, 10**4, 10**0]

    def __init__(self, sv_string):
        self.sv, self.sv_ar = self.sv_string_to_ver(sv_string)

    @staticmethod
    def sv_string_to_ver(sv_string):
        if sv_string is None:
            return None

        if type(sv_string) is not str:
            raise ValueError('Bad semantic version - must be string: |{0}|'
                             .format(sv_string))

        sv_ar = sv_string.split('.')
        if len(sv_ar) > 3 or len(sv_ar) == 0:
            raise ValueError('Bad semantic version string: |{0}|'
                             .format(sv_string))
        try:
            sv_ar = [int(s) for s in sv_ar]
            sv_val = SemanticVersion.sv_ar_to_sv(sv_ar)
        except ValueError:
            raise ValueError('Bad semantic version string: |{0}|'
                             .format(sv_string))
        sv_ar = [a1+a2 for a1, a2 in
                 zip_longest(sv_ar, [0, 0, 0], fillvalue=0)]
        return sv_val, sv_ar

    @staticmethod
    def sv_ar_to_sv(sv_ar):
        sv_zip = zip_longest(SemanticVersion.mult, sv_ar, fillvalue=0)
        sv_val = [m * v for m, v in sv_zip]
        return sv_val

    def __lt__(self, other):
        return self.sv < other.sv

    def __le__(self, other):
        return self.sv <= other.sv

    def __eq__(self, other):
        return self.sv == other.sv

    def __ge__(self, other):
        return self.sv >= other.sv

    def __gt__(self, other):
        return self.sv > other.sv

    def __str__(self):
        return '.'.join([str(v) for v in self.sv_ar])

    def bump_ver(self, ver_type):
        assert ver_type in SEMANTIC_VERSIONS
        if ver_type == MAJOR:
            pos = 0
        elif ver_type == MINOR:
            pos = 1
        else:
            pos = 2
        self.sv_ar[pos] += 1
        self.sv = self.sv_ar_to_sv(self.sv_ar)
        return self


