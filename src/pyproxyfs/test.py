#!/usr/bin/python

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

"""
Simple tests for pyproxyfs
"""

__author__ = "Nic Ferrier, <nic@ferrier.me.uk>"

import unittest
from pyproxyfs import TestFS
from pyproxyfs import Filesystem

def show_conf_files(dirtolist, filesystem=None):
    """Filter the filesystem."""
    if not filesystem:
       filesystem = Filesystem()
    files = filesystem.listdir(dirtolist)
    import re
    cfgpat = re.compile(".*\\.cfg$")
    cfg_files = [fn for fn in files if cfgpat.match(fn)]
    return cfg_files

class FilesystemTest(unittest.TestCase):
    def setUp(self):
        self.testfs = TestFS({
                "f1": "hello world!!!",
                "f2": "",
                "d1": "",
                "d1/f1": "# empty file",
                "d1/f2": "/* empty file */",
                "d1/s1/f3": "# empty file",
                })

    def test_listdir(self):
        self.assert_(
            self.testfs.listdir(".") == ['f1', 'f2', 'd1']
            )
        self.assert_(
            self.testfs.listdir("d1") == ['f1', 's1', 'f2']
            )
        self.assert_(
            self.testfs.listdir("d1/s1") == ['f3']
            )
        
    def test_rename(self):
        self.testfs.rename("f1", "g1")
        self.assert_(
            self.testfs.listdir(".") == ['f2', 'g1', 'd1']
            )

    def test_rename_into_dir(self):
        self.testfs.rename("f1", "d1/g1")
        self.assert_(
            self.testfs.listdir(".") == ['f2', 'd1']
            )
        self.assert_(
            self.testfs.listdir("d1") == ['f1', 's1', 'f2', 'g1'],
            self.testfs.listdir("d1")
            )

    def test_rename_across_dirs(self):
        renametestfs = TestFS({
                "f1": "hello world!!!",
                "f2": "",
                "d1": "",
                "d1/f1": "# empty bash file",
                "d1/f2": "/* empty file */",
                "d1/s1/f3": "# empty python file",
                "d1/s1/bb": "# empty bash file",
                "d1/s3/f3": "# empty file",
                "d2/f1": "# another empty file",
                })

        renametestfs.rename("d1/f2", "d2/different.3")
        self.assert_(
            renametestfs.listdir("d2") == ['f1', 'different.3'],
            renametestfs.listdir("d2")
            )
        self.assert_(
            renametestfs.listdir("d1") == ["s3","f1","s1"],
            renametestfs.listdir("d1")
            )

        renametestfs.rename("d1/s1/f3", "d1/s3/aa")
        self.assert_(
            renametestfs.listdir("d1/s3") == ['aa', 'f3'],
            renametestfs.listdir("d1/s3")
            )
        self.assert_(
            renametestfs.listdir("d1/s1") == ["bb"],
            renametestfs.listdir("d1/s1")
            )
        print "\n", renametestfs.files

    def test_open(self):
        self.assert_(
            self.testfs.open("f1").read() == 'hello world!!!'
            )

        self.testfs.rename("f1", "g1")
        self.assert_(
            self.testfs.open("g1").read() == 'hello world!!!'
            )

    def test_contextopen(self):
        with self.testfs.open("f1") as fd:
            self.assert_(fd.read() == 'hello world!!!')

    def test_glob(self):
        self.assert_(
            self.testfs.glob("*f*") == ['d1/f1', 'd1/f2', 'd1/s1/f3', 'f1', 'f2']
            )

    def test_status(self):
        self.assert_(self.testfs.isdir("d1"))
        self.assert_(self.testfs.isdir("d1/s1"))
        self.assert_(self.testfs.exists("d1/f1"))
        self.assert_(self.testfs.exists("d1"))
        self.assert_(self.testfs.exists("d1/s1/f3"))
        self.assert_(self.testfs.exists("d1/s1"))
        self.assert_(self.testfs.isdir("d1/s1"))

    def test_rm(self):
        self.testfs.remove("f1")
        self.assert_(not self.testfs.exists("f1"))
        
        self.testfs.remove("d1/f1")
        self.assert_(not self.testfs.exists("d1/f1"))
        self.assert_(self.testfs.exists("d1"))

    def test_show_conf_files(self):
        fs = TestFS({
            "somedir/a.cfg": "",
            "somedir/a.txt": "",
            "somedir/b.cfg": "",
            "somedir/run.py": ""
            })
        self.assert_(
            show_conf_files("somedir", filesystem=fs) == ['a.cfg', 'b.cfg']
            )

if __name__ == "__main__":
    unittest.main()

# End
