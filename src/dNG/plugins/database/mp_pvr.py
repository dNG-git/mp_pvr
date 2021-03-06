# -*- coding: utf-8 -*-

"""
MediaProvider
A device centric multimedia solution
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?mp;pvr

The following license agreement remains valid unless any additions or
changes are being made by direct Netware Group in a written form.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(mpPvrVersion)#
#echo(__FILEPATH__)#
"""

# pylint: disable=unused-argument

from dNG.database.schema import Schema
from dNG.module.named_loader import NamedLoader
from dNG.plugins.hook import Hook

def after_apply_schema(params, last_return = None):
    """
Called for "dNG.pas.Database.applySchema.after"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
    """

    container_class = NamedLoader.get_class("dNG.database.instances.MpUpnpPvrContainerResource")
    Schema.apply_version(container_class)

    resource_class = NamedLoader.get_class("dNG.database.instances.MpUpnpPvrRecordingResource")
    Schema.apply_version(resource_class)

    return last_return
#

def before_apply_schema(params, last_return = None):
    """
Called for "dNG.pas.Database.applySchema.before"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
    """

    resource_class = NamedLoader.get_class("dNG.database.instances.MpUpnpPvrRecordingResource")
    if (resource_class is not None): resource_class.before_apply_schema()

    return last_return
#

def load_all(params, last_return = None):
    """
Load and register all SQLAlchemy objects to generate database tables.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:since: v0.1.00
    """

    NamedLoader.get_class("dNG.database.instances.MpUpnpPvrContainerResource")
    NamedLoader.get_class("dNG.database.instances.MpUpnpPvrRecordingResource")

    return last_return
#

def register_plugin():
    """
Register plugin hooks.

:since: v0.1.00
    """

    Hook.register("dNG.pas.Database.applySchema.after", after_apply_schema)
    Hook.register("dNG.pas.Database.applySchema.before", before_apply_schema)
    Hook.register("dNG.pas.Database.loadAll", load_all)
#

def unregister_plugin():
    """
Unregister plugin hooks.

:since: v0.1.00
    """

    Hook.unregister("dNG.pas.Database.applySchema.after", after_apply_schema)
    Hook.unregister("dNG.pas.Database.applySchema.before", before_apply_schema)
    Hook.unregister("dNG.pas.Database.loadAll", load_all)
#
