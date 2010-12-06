from distutils.core import setup

setup(
    name = 'distPND',
    version = '0.1',
    description = "Extensions to Python's Distutils to build PND files",
    long_description = open('README.rst').read(),
    author = 'Randy Heydon',
    author_email = 'randy.heydon@clockworklab.net',
    packages = ['distpnd'],
    license = 'MIT',
)
