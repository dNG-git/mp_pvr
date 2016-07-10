# -*- coding: utf-8 -*-
##j## BOF

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
59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(mpPvrVersion)#
#echo(__FILEPATH__)#
"""

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import VARCHAR

from .mp_upnp_resource import MpUpnpResource

class MpUpnpPvrContainerResource(MpUpnpResource):
#
	"""
"MpUpnpPvrContainerResource" represents an database UPnP PVR container
entry.
s
:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    mp
:subpackage: pvr
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	__tablename__ = "{0}_mp_upnp_pvr_container_resource".format(MpUpnpResource.get_table_prefix())
	"""
SQLAlchemy table name
	"""
	db_instance_class = "dNG.data.upnp.resources.MpEntryPvrContainer"
	"""
Encapsulating SQLAlchemy database instance class name
	"""
	db_schema_version = 1
	"""
Database schema version
	"""

	id = Column(VARCHAR(32), ForeignKey(MpUpnpResource.id), primary_key = True)
	"""
mp_upnp_pvr_container_resource.id
	"""
	manager_id = Column(VARCHAR(255), index = True)
	"""
mp_upnp_pvr_container_resource.manager_id
	"""

	__mapper_args__ = { "polymorphic_identity": "MpUpnpPvrContainerResource" }
	"""
sqlalchemy.org: Other options are passed to mapper() using the
__mapper_args__ class variable.
	"""
#

##j## EOF