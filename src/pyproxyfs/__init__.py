# pyproxyfs - a very lightweight proxy filesystem class
# Copyright (C) 2010  Nic Ferrier <nic@ferrier.me.uk>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import os.path

class Filesystem(object):
    """Base filesystem interface also the base implementation.

    The implementation talks very simply to the normal Python functions.
    """
    def rename(self, oldpath, newpath):
        os.rename(oldpath, newpath)

    def listdir(self, path):
        return os.listdir(path)

    def open(self, path, mode="r"):
        return open(path, mode)

    def iglob(self, path):
        import glob
        return glob.iglob(path)

    def glob(self, path):
        return list(self.iglob(path))

    def exists(self, path):
        return os.path.exists(path)

    def isdir(self, path):
        return os.path.isdir(path)


def _mergedict(a, b):
    """Recusively merge the 2 dicts.

    Destructive on argument 'a'.
    """
    for p, d1 in b.iteritems():
        if p in a:
            if d1 == "":
                continue
            _mergedict(a[p], d1)
        else:
            a[p] = d1
    return a

class TestFS(Filesystem):
    def __init__(self, data):
        super(TestFS, self).__init__()
        self.paths = data
        self.files = {}
        # Make the path: object into a nested dict setup
        for name,data in data.iteritems():
            paths = name.split("/")
            d = {}
            d[paths[-1]] = data
            for p in reversed(paths[:-1]):
                d = { p: d }
            _mergedict(self.files, d)

    def open(self, path, mode=None):
        path = path.split("/")
        d = self.files
        for p in path:
            d = d[p]
        obj = d
        class grd():
            def __enter__(self):
                return  self
            def __exit__(self, type, values, traceback):
                pass
            def read(self):
                return obj
        return grd()

    def rename(self, old, new):
        path = old.split("/")
        d = self.files
        lastd = None
        for p in path:
            lastd = d
            d = d[p]
        del lastd[p]
        obj = d
        np = new.split("/")
        d = {}
        d[np[-1]] = obj
        for p in reversed(np[:-1]):
            d = { p: d }
        _mergedict(self.files, d)
        return self
        
    def _listdir(self, path):
        if path == ".":
            for i in self.files:
                yield i
        else:
            paths = path.split("/")
            d = self.files
            for p in paths:
                d = d[p]
            for i in d:
                yield i

    def listdir(self, path):
        return list(self._listdir(path))

    def iglob(self, path):
        import fnmatch
        for p in sorted(self.paths.keys()):
            if fnmatch.fnmatch(p, path):
                yield p

    def exists(self, path):
        try:
            self.paths[path]
        except KeyError:
            return False
        else:
            return True

    def isdir(self, path):
        """This works by pure convention.

        You must declare a path entry for the dir that has no content:

           "/home/nic/projects/special": "",
           "/home/nic/projects/special/file.c": "#include <stdio.h>",

        "/home/nic/projects/special" will be considered a directory,
        whereas "/home/nic/projects/special/file.c" will not.
        """
        if self.exists(path):
            content = self.paths[path]
            return content == ""
        return False

# End
