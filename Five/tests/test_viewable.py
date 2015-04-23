##############################################################################
#
# Copyright (c) 2004, 2005 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Unit tests for the viewable module.

$Id: test_viewable.py 61434 2005-11-08 15:45:35Z yuppie $
"""
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

def test_defaultView():
    """
    Testing default view functionality

      >>> from zope.app.tests.placelesssetup import setUp, tearDown
      >>> setUp()

    Take a class Foo and an interface IFoo:

      >>> class Foo:
      ...     pass

      >>> from zope.interface import Interface
      >>> class IFoo(Interface):
      ...     pass

    Set up a default view for IFoo:

      >>> from zope.app import zapi
      >>> pres = zapi.getGlobalService('Presentation')
      >>> from zope.publisher.interfaces.browser import IBrowserRequest

    and default view names for everything and IFoo objects in particular:

      >>> pres.setDefaultViewName(None, IBrowserRequest, u'index.html')
      >>> pres.setDefaultViewName(IFoo, IBrowserRequest, u'foo.html')

    Now take a BrowserDefault for an instance of Foo::

      >>> foo = Foo()
      >>> from Products.Five.viewable import BrowserDefault
      >>> bd = BrowserDefault(foo)

    For now the default view name is index.html, like we set above:

      >>> from Products.Five.traversable import FakeRequest
      >>> request = FakeRequest()

      >>> obj, path = bd.defaultView(request)
      >>> obj is foo
      True
      >>> path
      [u'index.html']

    until we mark the object with IFoo:

      >>> from zope.interface import directlyProvides
      >>> directlyProvides(foo, IFoo)
      >>> obj, path = bd.defaultView(request)
      >>> obj is foo
      True
      >>> path
      [u'foo.html']


    Clean up:

      >>> tearDown()
    """

def test_suite():
    import unittest
    from Products.Five.testing.doctest import DocTestSuite
    from Testing.ZopeTestCase import FunctionalDocFileSuite
    return unittest.TestSuite((
            DocTestSuite(),
            FunctionalDocFileSuite('viewable.txt',
                                   package="Products.Five.tests",),
            ))

if __name__ == '__main__':
    framework()
