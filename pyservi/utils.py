import globals as g

def qprint(*args, **kwargs):
    # quiet print - relies on 'import globals as g'
    if g.quiet:
        print('qprint')
        return
    print(*args, **kwargs)