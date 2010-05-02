# pyproxyfs - a lightweight filesystem proxy object

The aim of pyproxyfs is to provide a filesystem class that you can use
for doing much of your file handling... but that can easi;ly be mocked
for specific testing purposes.

If, instead of using open, os.rename and os.listdir you use the
pyproxyfs equivalents you can expect to be able to make a simple
filesystem using the builtin TestFS class and write tests around that.

For example:

    def show_conf_files(dirtolist, filesystem=None):
        from pyproxyfs import Filesystem
        if not filesystem:
           filesystem = Filesystem()
        files = filesystem.listdir(dirtolist)
        import re
        cfgpat = re.compile(".*\\.cfg$")
        cfg_files = [fn for fn in files if cfgpat.match(fn)]
        return cfg_files


this might be your application code.

You could then test it relatively simply:

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


## Limitations

The pyproxyfs is not designed to be a full filesystem proxy, it's just
a simple and quick way to test.

There is no way to write to the TestFS system yet; native filesystem
writes work through the proxy tho as it just uses `open` directly.
