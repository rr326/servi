import os
from glob import glob


def import_commands():
    all_list=[]
    for f in glob(os.path.dirname(__file__)+'/*.py'):
        if os.path.isfile(f) and not os.path.basename(f).startswith('_'):
            all_list.append(os.path.basename(f)[:-3])

    return all_list

__all__ = import_commands()
print('Commands: __all__: {0}'.format(__all__))
