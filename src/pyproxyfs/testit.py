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

from pyproxyfs import TestFS

def testfs(*args):
    """
    >>> testfs().listdir(".")
    ['f1', 'f2', 'd1']
    >>> testfs().listdir("d1")
    ['f1', 'f2']
    >>> testfs().rename("f1", "g1").listdir(".")
    ['f2', 'g1', 'd1']
    >>> testfs().open("f1").read()
    'hello world!!!'
    >>> testfs().rename("f1", "g1").open("g1").read()
    'hello world!!!'
    >>> testfs("contextopen", "f1").read()
    'hello world!!!'
    >>> testfs().glob("*f*")
    ['d1/f1', 'd1/f2', 'f1', 'f2']
    >>> testfs().isdir("d1")
    True
    >>> testfs().isdir("d1/f1")
    False
    """
    testfs = TestFS({
            "f1": "hello world!!!",
            "f2": "",
            "d1": "",
            "d1/f1": "# empty file",
            "d1/f2": "/* empty file */",
            })
    if args and args[0] == "contextopen":
        with testfs.open(args[1]) as fd:
            return fd
    else:
        return testfs
            
if __name__ == "__main__":
    import sys
    print sys.path
    import doctest
    doctest.testmod()

# End
