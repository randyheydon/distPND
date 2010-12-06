=======
distPND 
=======
    Build PNDs with Distutils

This project provides Distutils commands that can be used to create `PND files`_ for the `Pandora handheld`_.

Two commands are provided: gen_pxml and bdist_pnd.  gen_pxml will generate a PXML file based on information contained in the setup script and provided as options.  bdist_pnd will assemble a PND file by taking advantage of the install command.  Therefore, any options given to install (or its subcommands) in the setup.cfg will be reflected in the PND.


Installation
============

Python, version 2.4 to 2.7
--------------------------
First off, to use this you obviously need Python installed.  distPND has been used in Python versions 2.6 and 2.7, but should work in versions as old as 2.4 (but definitely not older than that).  No support for 3.x will be added in the forseeable future, as the Pandora doesn't yet even have it available.

python setup.py install
-----------------------
Install this package through the standard Python installation mechanism.  Since this is so standard, you can read more about it in the `Python package installation`_ documentation. 

mksquashfs/mkisofs
------------------
Without these commands, distPND can still make PND directories - folders filled with files that are read by the PND system.  However, the standard way to distribute a PND is as a single file; to do that, you'll need one or both of these installed.  Most distros have mksquashfs available in a package called "squashfs-tools" (make sure it's version 4.0 or later); this is the preferred package format.  If you would rather use an iso-format PND, mkisofs is available in "cdrkit" or "cdrtools".


Using in your project
=====================

Create the setup.py script
--------------------------
Again, this is just part of the standard Python installation mechanism.  You can read about how to make a setup script in the `Python package distribution`_ documentation.  If you find you need more control over the behaviour of your setup script, you can instead use setuptools_.

Specify command-packages
------------------------
Your setup script must be made aware that these commands are available.  The easiest way to this is in the setup.cfg file: under the heading [global], include the line "command-packages=distpnd".  Alternatively, this can be specified on the command line as an option to the setup script in the form "python setup.py --command-packages distpnd *command*".

Specify PND-specific options
----------------------------
All options can be specified in setup.cfg file under the appropriate heading.

Under the [gen_pxml] heading, you will want to specify a `standard category and subcategory`_ in the form of "categories=Category:Subcategory".  If a category is unspecified or non-standard, a warning will be printed.  Note that, though multiple categories and subcategories are supported, it will cause your PND to appear in multiple places in the Pandora's menu, which is weird.

Under the [bdist_pnd] heading, you will likely want to specify icon and info files ("icon=icon.png" and "info=info.html", respectively).  Both can instead be specified under the [gen_pxml] heading, but putting them here ensures they are copied into the PND.  Also, if you find gen_pxml's autogeneration too limiting, you can write your own PXML file and tell bdist_pnd to use it with "pxml=PXML.xml"; otherwise, bdist_pnd will call gen_pxml to create a PXML file for it to use.

Many more options are available for both commands.  As with any Distutils command, all options can be viewed using "python setup.py --help *command*".

Examples
--------
distPND has been used in at least two projects so far: `The Lonely Tower`_, by the author, and Sparks_, by haltux.  Both should give you an idea of how to use distPND in your own projects.


Limitations
===========
distPND is still early and not-very-well-tested software, so it's not perfect.  Here are some of the notable limitations:

* Does not respect dry-run or no-clobber.
    No avoidance of file writing and overwriting has been coded in to bdist_pnd yet.  Fortunately, this can be worked around: by default, bdist_pnd only writes to the directories "build", "build_pnd", and "dist".  As long as you have nothing important stored in those folders, you need not worry about accidental overwrites.

* Cross compiling is untested.
    Though pure Python is cross-platform, extension modules written in C or Cython need to be compiled to run on the Pandora.  I think that this can be done by setting the "compiler" option to the build command to a cross compiler, but this is untested and inelegant.  The easiest workaround is to just compile on the Pandora itself.

* No way to include external packages.
    The Pandora, by default, includes only a few non-standard Python libraries: Pygame, PyGTK, Numeric, Cairo, DBus, and Fuse.  If your project requires any other external libraries, they have to be distributed in your PND, but it's currently not possible to make bdist_pnd pull them in.  This is a feature of setuptools_, and I hope to make distPND take advantage of it soon.

* Packages cannot import each other.
    If your project contains multiple separate packages, they will currently not be able to import each other.  If installed normally, all packages would be on the path, and therefore accessible to each other.  Many projects contain only one top-level package, and for them this issue would not appear; however, once external package installation is added, this will be a real problem.  I hope to fix this soon-ish.

* data_files behaves strangely; use package_data where possible.
    I don't fully understand the workings of the data_files option to the setup function; therefore, I don't know where in the PND those files will end up.  Files specified in package_data behave a lot more predictably, so I recommend you use those instead.


.. _PND files: http://pandorawiki.org/PND
.. _Pandora handheld: http://openpandora.org
.. _Python package installation: http://docs.python.org/install
.. _Python package distribution: http://docs.python.org/distutils
.. _setuptools: http://packages.python.org/distribute
.. _standard category and subcategory: http://standards.freedesktop.org/menu-spec/latest/apa.html
.. _The Lonely Tower: http://randy.heydon.selfip.net/Programs/The%20Lonely%20Tower/V2
.. _Sparks: http://github.com/haltux/Sparks
