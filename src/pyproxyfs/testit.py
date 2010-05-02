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

def testfs():
    """
    >>> testfs().listdir(".")
    ['f1', 'f2', 'd1']
    >>> testfs().listdir("d1")
    ['f1', 'f2']
    >>> testfs().rename("f1", "g1").listdir(".")
    ['f2', 'g1', 'd1']
    >>> testfs().open("f1").read()
    'hello world!!!'
    """
    return TestFS({
            "f1": "hello world!!!",
            "f2": "",
            "d1/f1": "",
            "d1/f2": "",
            })
            
if __name__ == "__main__":
    import doctest
    doctest.testmod()

# End
