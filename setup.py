from setuptools import setup
#from setuptools import find_packages
#from distutils.core import setup

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: System :: Filesystems',
]

setup(
    name = "PyProxyFS",
    version = "0.7",
    description = "Simple filesystem abstraction",
    long_description = """A proxy filesystem interface with a native
filesystem implementation and a very simple test in-memory filesystem.""",
    packages = ["pyproxyfs"],
    test_suite = "pyproxyfs",

    # Metadata
    license = "GNU GPL v3",
    author = "Nic Ferrier",
    author_email = "nic@ferrier.me.uk",
    url = "http://github.com/nicferrier/pyproxyfs",
    download_url="http://github.com/nicferrier/pyproxyfs/downloads",
    platforms = ["any"],
    package_dir = {"":"src"},
    classifiers =  classifiers
    )
