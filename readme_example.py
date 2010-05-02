
from os.path import join as joinpath
from os.path import dirname
import sys
sys.path = sys.path + [joinpath(dirname(__file__), "src")]

def show_conf_files(dirtolist, filesystem=None):
    from pyproxyfs import Filesystem
    if not filesystem:
       filesystem = Filesystem()
    files = filesystem.listdir(dirtolist)
    import re
    cfgpat = re.compile(".*\\.cfg$")
    cfg_files = [fn for fn in files if cfgpat.match(fn)]
    return cfg_files    


def test_show_conf_files():
    """
    >>> test_show_conf_files()
    ['a.cfg', 'b.cfg']
    """
    from pyproxyfs import TestFS
    fs = TestFS({
        "somedir/a.cfg": "",
        "somedir/a.txt": "",
        "somedir/b.cfg": "",
        "somedir/run.py": ""
        })
    return show_conf_files("somedir", filesystem=fs)
            
if __name__ == "__main__":
    import doctest
    doctest.testmod()
