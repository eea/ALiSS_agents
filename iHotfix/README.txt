
This product dynamically patches Zope to fix four problems: the global
request, the accept language, unicode for ZPT and mx.DateTime. Details
below.


Installation
============

This product requires the itools Python package. Download the last version
from http://sf.net/projects/lleu

Then just unpack the tarball in the 'Products' directory.


1. Global Request
=================

It makes the request and response objects globally available through the
"context".

    >>> from itools.zope import get_context
    >>> context = get_context()
    >>> request, response = context.request, context.response

In some situations (within the __getattr__ and __of__ methods, for instance)
this is the only way to get the request and response objects. It is also more
elegant than to pass them as parameters to to get them through acquisition.

This method is thread safe.


2. Accept Language
==================

Adds the variables AcceptLanguage and AcceptCharset to the request object.
They provide a higher level interface than HTTP_ACCEPT_LANGUAGE and
HTTP_ACCEPT_CHARSET.


3. Unicode for ZPT
==================

Fixes Zope to enable the use of Unicode with Page Templates.


4. locale
=========

XXX The information below is obsolete

Multilingual products need a place to store the message catalogs, both
Localizer and iKaaro use the convention to store them within the product,
in the 'locale' directory, for example:

  locale/en.po
  locale/es.po
  locale/fr.po

It is iHotfix which provides the means to access the catalogs this way. Use
it in your own product like:

  from Products.iHotfix import N_, translation
  _ = translation(globals())

Put the two lines above in your product to get the functions '_' and 'N_',
the developer familiarized with gettext will recognize them. What they do
is:

  _(message, language=None)
  Looks up a translation for the message in the message catalog and returns
  it if it exists, otherwise returns the message. The parameter 'language'
  says which catalog to use, if it is 'None', the language negotiation
  machinery will be triggered to choose one.

  N_(message, language=None)
  Always returns the message itself. This function is used to markup a message
  so the extraction scripts detect it to feed the message catalogs.


Author and License
==================

  Copyright (C) 2001-2004  Juan David Ib��ez Palomar (jdavid@itaapy.com)

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
