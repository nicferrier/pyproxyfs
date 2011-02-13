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

    def remove(self, path):
        os.remove(path)

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
            if not isinstance(d1, dict):
                continue
            _mergedict(a[p], d1)
        else:
            a[p] = d1
    return a

class TestFS(Filesystem):
    def __init__(self, data):
        super(TestFS, self).__init__()
        # 'paths' is pretty much what is passed in
        self.paths = data
        # 'files' is the decomposed paths -> json structure
        # eg: "/a/b" is stored as a key "a" with a dict containing a key "b":
        #   {"a": {"b": "filecontent"}}
        self.files = {}
        # Make the path: object into a nested dict setup
        for name,data in data.iteritems():
            paths = name.split("/")
            if paths[0] == "":
                paths = paths[1:]
            d = {}
            d[paths[-1]] = data
            for p in reversed(paths[:-1]):
                d = { p: d }
            _mergedict(self.files, d)

    def open(self, path, mode=None):
        path = path.split("/")
        if path[0] == "":
            path = path[1:]
        d = self.files
        for p in path:
            if not p:
                continue
            d = d[p]
        obj = d
        class grd():
            def __enter__(self):
                return  self
            def __exit__(self, type, values, traceback):
                pass
            def read(self):
                return obj
            def readline(self, size=-1):
                if not getattr(self, "lineno", False):
                    setattr(self, "lineno", 0)
                lines = obj.split("\n")
                if self.lineno == len(lines):
                    return "\n"
                if self.lineno > len(lines):
                    raise IOError()
                line = lines[self.lineno]
                self.lineno = self.lineno + 1
                return "%s\n" % line
        return grd()

    def rename(self, old, new):
        path = old.split("/")
        if path[0] == "":
            path = path[1:]
        d = self.files
        lastd = None
        for p in path:
            lastd = d
            d = d[p]

        del lastd[p]

        obj = d
        np = new.split("/")
        if np[0] == "":
            np = np[1:]
        d = {}
        d[np[-1]] = obj
        for p in reversed(np[:-1]):
            d = { p: d }
        _mergedict(self.files, d)
        return self

    def remove(self, path):
        """Deletes just the end point"""
        def _path_find(path_parts, fs):
            for p,f in fs.iteritems():
                if p == path_parts[0]:
                    if len(path_parts) == 1:
                        del fs[p]
                        return
                    else:
                        return _path_find(path_parts[1:], f)
            raise KeyError()

        pt = path.split("/")
        return _path_find(pt if pt[0] != "" else pt[1:], self.files)

    def _listdir(self, path):
        if path == ".":
            for i in self.files:
                yield i
        else:
            paths = path.split("/")
            if paths[0] == "":
                paths = paths[1:]
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

    def _path(self, path):
        """Functional/recursive path finder.

        Raises KeyError if the path is not found
        """
        def _path_find(path_parts, fs):
            for p,f in fs.iteritems():
                if p == path_parts[0]:
                    if len(path_parts) == 1:
                        return f
                    else:
                        return _path_find(path_parts[1:], f)
            raise KeyError()

        pt = path.split("/")
        return _path_find(pt if pt[0] != "" else pt[1:], self.files)

    def exists(self, path):
        """Functional (recursive) exists on the path structures"""
        try:
            self._path(path)
        except KeyError:
            return False
        else:
            return True

    def isdir(self, path):
        """Is the path a directory?

        A path is a directory if it holds a dictionary.
        """
        if self.exists(path):
            content = self._path(path)
            # Not sure this is the best attribute to check for.
            return hasattr(content, "keys")
        return False

# End
