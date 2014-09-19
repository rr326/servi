import os.path
import yaml

"""
This is an ugly, parameterized version of pathfor, and a getconfig() which
relies on it. I need it since the other pathfor uses config parameters
(which this bootstraps).

Only use this in the config module.
After that, use commands.utils.utils.pathfor()
"""


def pathfor(fname, source, template, master, template_dir, master_dir):
    assert source in [template, master]

    if source == template:
        path = os.path.normpath(os.path.join(template_dir, fname))
    else:  # MASTER
        path = os.path.normpath(os.path.join(master_dir, fname))

    return path


def getconfig(fname, template, master, template_dir, master_dir):
    try:
        with open(pathfor(fname, master, template, master,
                  template_dir, master_dir)) as f:
            data = yaml.load(f)
    except FileNotFoundError:
        with open(pathfor(fname, template, template, master,
                  template_dir, master_dir)) as f:
            data = yaml.load(f)

    return data