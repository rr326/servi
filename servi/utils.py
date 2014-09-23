import os
import globals as g
from servi_exceptions import MasterNotFound


def qprint(*args, **kwargs):
    # quiet print - relies on 'import globals as g'
    if g.quiet:
        print('qprint')
        return
    print(*args, **kwargs)


def file_exists(path):
    return os.path.isfile(path) and os.access(path, os.R_OK)


def find_ancestor_with(starting_dir, dirname):
    """
    returns first ancestor of starting_dir that contains dirname
    (returns abspath())
    returns None if not found
    """
    cur_dir = os.path.abspath(starting_dir)

    while cur_dir != '/':
        if os.path.exists(os.path.join(cur_dir, dirname)):
            return cur_dir
        cur_dir = os.path.abspath(os.path.normpath(os.path.join(cur_dir, '..')))

    return None


def find_master_dir(fail_ok=False):
    """
    Returns the master dir with the following signature at or above cwd:
    MASTER_DIR
        \servi
            \servi_templates
    raises MasterNotFound if not found
    (if failok, and not found, returns None)
    """
    servi_dir = find_ancestor_with(os.getcwd(), 'servi')
    if (not servi_dir or
            not os.path.exists(
                os.path.join(servi_dir, 'servi/servi_templates'))):

        if fail_ok:
            return None
        else:
            raise MasterNotFound(os.getcwd())
    return servi_dir