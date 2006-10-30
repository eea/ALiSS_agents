# -*- coding: utf-8 -*-
# The contents of this file are subject to the Mozilla Public
# License Version 1.1 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of
# the License at http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS
# IS" basis, WITHOUT WARRANTY OF ANY KIND, either express or
# implied. See the License for the specific language governing
# rights and limitations under the License.
#
# The Initial Owner of the Original Code is European Environment
# Agency (EEA).  Portions created by Finsiel Romania are
# Copyright (C) European Environment Agency. All
# Rights Reserved.
#
# Authors:
# Alexandru Ghica - Finsiel Romania
# Antonio De Marinis - EEA
# Sasha Vinčić - Systemvaruhuset

#Python imports

#Zope imports
from ImageFile      import ImageFile

#Product imports
from Products.EEAALiSS import eea_aliss


def initialize(context):
    """ initialize the EEAALiSS component """

    #EEAALiSS
    context.registerClass(
        eea_aliss.EEAALiSS,
        constructors = (eea_aliss.manage_addEEAALiSS_html, eea_aliss.manage_addEEAALiSS),
        icon = 'images/EEAALiSS.gif'
        )

misc_ = {
    #zope object incons
    'EEAALiSS.gif': ImageFile('images/EEAALiSS.gif', globals()),
    }
