#!/usr/bin/env python
'''
Tests for fastqutils / docutils
'''

import os
import unittest
import doctest
import StringIO

import hpt
import hpt.fastx


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(hpt))
    tests.addTests(doctest.DocTestSuite(hpt.fastx))
    return tests

if __name__ == '__main__':
    unittest.main()
