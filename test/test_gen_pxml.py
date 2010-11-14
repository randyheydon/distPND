#!/usr/bin/env python2
"""Tests the gen_pxml command.
Note that there doesn't seem to be a way to test for warnings, nor to prevent them from appearing, so just ignore them I guess."""
import unittest, os
from distutils.core import run_setup
from distutils.errors import DistutilsOptionError, DistutilsFileError


class BaseTester(unittest.TestCase):
    "Provides functions useful to all test classes here."
    def setUp(self):
        self.setup_name = 'setup.py'
        self.setup_contents = """
import sys
sys.path.insert(0,'..')
from distutils.core import setup
setup(
    command_packages = 'distpnd',
    {0}
)"""
        self.cfg_name = 'setup.cfg'
        self.cfg_contents = ''
        self.to_clean = set() #Set of files to be removed in tearDown.

    def tearDown(self):
        for f in self.to_clean:
            os.remove(f)

    def _mksetup(self):
        with open(self.setup_name, 'w') as s, open(self.cfg_name, 'w') as c:
            s.write(self.setup_contents)
            c.write(self.cfg_contents)
        self.to_clean.add(self.setup_name)
        self.to_clean.add(self.cfg_name)
        self.setup_obj = run_setup(self.setup_name)



class TestGeneral(BaseTester):
    def testBasic(self):
        self.setup_contents = self.setup_contents.format("""
            name = 'Super Dude',
            version = '0.1.butts',
            description = 'Real super.',
            scripts = ['runitall'],""")
        self.cfg_contents='[gen_pxml]\ncategories=Game'
        self._mksetup()
        self.setup_obj.run_command('gen_pxml')
        self.to_clean.add('PXML.xml')


    def testOverwriting(self):
        self.setup_contents = self.setup_contents.format("""
            name = 'Super Dude',
            version = '0.1.butts',
            description = 'Real super.',
            scripts = ['runitall'],""")
        self.cfg_contents='[gen_pxml]\ncategories=Game'

        self._mksetup()
        self.setup_obj.run_command('gen_pxml')
        self.to_clean.add('PXML.xml')

        self._mksetup()
        self.assertRaises(DistutilsFileError, self.setup_obj.run_command, 'gen_pxml')

        self.cfg_contents='[gen_pxml]\ncategories=Game\nforce=1'
        self._mksetup()
        self.setup_obj.run_command('gen_pxml')


class TestInsufficientInfo(BaseTester):
    def testNoName(self):
        self.setup_contents = self.setup_contents.format("""
            version = '0.1.butts',
            description = 'Real super.',
            scripts = ['runitall'],""")
        self._mksetup()
        self.assertRaises(DistutilsOptionError, self.setup_obj.run_command, 'gen_pxml')



if __name__=='__main__':
    unittest.main()
