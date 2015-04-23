# -*- coding: ISO-8859-1 -*-
# Copyright (C) 2000-2004  Juan David Ib��ez Palomar <jdavid@itaapy.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

# Import from iHotfix
from Products.iHotfix import translation


def N_(message, language=None):
        """
    Used to markup a string for translation but without translating it,
    this is known as deferred translations.
    """
    return message


dummy = N_


# XXX This module is kept only for backwards compatibility with
# Localizer <= 1.1.0b1
