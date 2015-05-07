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

from sqlalchemy.event import listen
from sqlalchemy.schema import Column, DDL, ForeignKey
from sqlalchemy.types import INT, TEXT, VARCHAR

from dNG.pas.database.types.date_time import DateTime
from .mp_upnp_video_resource import MpUpnpVideoResource

class MpUpnpPvrRecordingResource(MpUpnpVideoResource):
#
	"""
"MpUpnpPvrRecordingResource" represents an database UPnP PVR recording
entry.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    mp
:subpackage: pvr
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	__tablename__ = "{0}_mp_upnp_pvr_recording_resource".format(MpUpnpVideoResource.get_table_prefix())
	"""
SQLAlchemy table name
	"""
	db_instance_class = "dNG.pas.data.upnp.resources.MpEntryPvrRecording"
	"""
Encapsulating SQLAlchemy database instance class name
	"""
	db_schema_version = 1
	"""
Database schema version
	"""

	id = Column(VARCHAR(32), ForeignKey(MpUpnpVideoResource.id), primary_key = True)
	"""
mp_upnp_pvr_recording_resource.id
	"""
	recording_status = Column(INT, index = True, nullable = False)
	"""
Recording status
	"""
	channel = Column(VARCHAR(255), index = True)
	"""
mp_upnp_pvr_recording_resource.channel
	"""
	summary = Column(TEXT, index = True)
	"""
mp_upnp_pvr_recording_resource.summary
	"""
	time_started = Column(DateTime, index = True, nullable = False)
	"""
mp_upnp_pvr_recording_resource.time_started
	"""
	time_finished = Column(DateTime, index = True, nullable = False)
	"""
mp_upnp_pvr_recording_resource.time_finished
	"""
	recorder = Column(VARCHAR(255), index = True)
	"""
mp_upnp_pvr_recording_resource.recorder
	"""

	__mapper_args__ = { "polymorphic_identity": "MpUpnpPvrRecordingResource" }
	"""
sqlalchemy.org: Other options are passed to mapper() using the
__mapper_args__ class variable.
	"""

	@classmethod
	def before_apply_schema(cls):
	#
		"""
Called before applying the SQLAlchemy generated schema to register the
custom DDL for PostgreSQL.

:since: v0.1.00
	"""

		create_postgresql_tsvector_index = "CREATE INDEX idx_{0}_mp_upnp_pvr_recording_resource_summary ON {0}_mp_upnp_pvr_recording_resource USING gin(to_tsvector('simple', summary));"
		create_postgresql_tsvector_index = create_postgresql_tsvector_index.format(cls.get_table_prefix())

		listen(cls.__table__,
		       "after_create",
		       DDL(create_postgresql_tsvector_index).execute_if(dialect = "postgresql")
		      )
	#
#

##j## EOF