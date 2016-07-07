#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
test_mailmerge.py
(c) Will Roberts   7 July, 2016

Test the mailmerge module.
'''

from __future__ import absolute_import, print_function, unicode_literals
import unittest
from jinja_mailmerge import mailmerge

class TestMailmerge(unittest.TestCase):
    '''
    Unit tests for the mailmerge module.
    '''

    def test_firstrun(self):
        s = 'aaaaaaBBBBaaaaa'
        self.assertEqual(list(mailmerge.firstrun(lambda x: x == 'B', s)),
                         [x for x in s if x == 'B'])

if __name__ == '__main__':
    unittest.main()
