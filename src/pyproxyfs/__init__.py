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

class Filesystem(object):
    """Base filesystem interface also the base implementation.

    The implementation talks very simply to the normal Python functions.
    """
    def rename(self, oldpath, newpath):
        os.rename(oldpath, newpath)

    def listdir(self, path):
        return os.listdir(path)

    def open(self, path, mode=None):
        return open(path, mode)

def _mergedict(a,b):
    """Recusively merge the 2 dicts.

    Destructive on argument 'a'.
    """
    def mergedict_(t, d):
        for p, d1 in d.iteritems():
            if p in t:
                mergedict_(t[p], d1)
            else:
                t[p] = d1
    mergedict_(a, b)
    return a

class TestFS(Filesystem):
    def __init__(self, data):
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
                return  obj
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

# End
