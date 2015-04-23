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
"""Five interfaces

$Id: interfaces.py 18584 2005-10-14 17:13:27Z regebro $
"""
from zope.interface import Interface, Attribute
from zope.component.interfaces import IServiceService
from zope.app.utility.interfaces import ILocalUtilityService

class IRegisterUtilitySimply(Interface):
    """Register utilities simply

    Allow local registrations of utilities, in a much simpler
    manner than Zope 3 does it currently.

    Note: The name of this interface is expressed as a verb
    (describing the action it expresses, namely registering
    utilities).  The reason for that is that the names *utility
    registry* (successor of the Zope 3 utility service) and *utility
    registration* (object in a registration stack, part of the
    complicated registration framework in Zope 3) have different
    connotations in Zope 3 than we want to express here.
    """

    def registerUtility(self, interface, utility, name=''):
        """Registers a utility in the local context"""
        # TODO Define an exception than is to be thrown when a local
        # utility of that interface and name is already registered.

    next = Attribute("The next local registry in the tree. This attribute "
                     "represents the parent of this registry node. If the "
                     "value is ``None``, then this registry represents the "
                     "root of the tree")

class IFiveSiteManager(IServiceService, IRegisterUtilitySimply):
    """Five site manager

    For the sake of forward-portability, registering utilities can be
    done directly on the site manager to cut out the middle man called
    utility service (this corresponds to Zope 3.1's understanding of
    site managers).  An implementation of this interface will probably
    delegate the work to an IFiveUtilityService component, though."""

class IFiveUtilityService(ILocalUtilityService, IRegisterUtilitySimply):
    """Five local utility service"""

# forwards compatability with Five 1.3
IFiveUtilityRegistry = IFiveUtilityService
