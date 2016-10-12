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
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(mpPvrVersion)#
#echo(__FILEPATH__)#
"""

from dNG.data.binary import Binary
from dNG.data.rfc.basics import Basics
from dNG.database.instances.mp_upnp_pvr_recording_resource import MpUpnpPvrRecordingResource as _DbMpUpnpPvrRecordingResource

from .mp_entry_video import MpEntryVideo

class MpEntryPvrRecording(MpEntryVideo):
#
	"""
"MpEntryPvrRecording" is used for UPnP PVR recording database entries.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    mp
:subpackage: pvr
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	_DB_INSTANCE_CLASS = _DbMpUpnpPvrRecordingResource
	"""
SQLAlchemy database instance class to initialize for new instances.
	"""
	RECORDING_STATUS_UNKNOWN = 0
	"""
Unknown recording status
	"""
	RECORDING_STATUS_FINISHED = 3
	"""
Finished recording the broadcast
	"""
	RECORDING_STATUS_FAILED = 4
	"""
Failed to record the broadcast
	"""
	RECORDING_STATUS_RECORDING = 2
	"""
Ongoing recording of a broadcast
	"""
	RECORDING_STATUS_PLANNED = 1
	"""
Planned broadcast recording
	"""
	TYPE_CDS_ITEM_PVR_VIDEO = 512
	"""
UPnP CDS PVR video type
	"""

	def _add_metadata_to_didl_xml_node(self, xml_resource, xml_node_path, parent_id = None):
	#
		"""
Uses the given XML resource to add the DIDL metadata of this UPnP resource.

:param xml_resource: XML resource
:param xml_base_path: UPnP resource XML base path (e.g. "DIDL-Lite
                      item")

:since:  v0.1.00
		"""

		MpEntryVideo._add_metadata_to_didl_xml_node(self, xml_resource, xml_node_path, parent_id)

		if (self.get_type() & MpEntryPvrRecording.TYPE_CDS_ITEM == MpEntryPvrRecording.TYPE_CDS_ITEM and xml_resource.get_node(xml_node_path) is not None):
		#
			entry_data = self.get_data_attributes("description", "channel", "summary", "time_started", "time_finished")

			if (entry_data['channel'] is not None): xml_resource.add_node("{0} upnp:callSign".format(xml_node_path), entry_data['channel'])

			if (entry_data['summary'] is not None):
			#
				if (entry_data['description'] is None): xml_resource.add_node("{0} dc:description".format(xml_node_path), entry_data['summary'])
				else:
				#
					xml_resource.change_node_value("{0} dc:description".format(xml_node_path), entry_data['summary'])
					xml_resource.add_node("{0} upnp:longDescription".format(xml_node_path), entry_data['description'])
				#
			#

			if (entry_data['time_started'] is not None): xml_resource.add_node("{0} upnp:recordedStartDateTime".format(xml_node_path), Basics.get_iso8601_datetime(entry_data['time_started']))
			if (entry_data['time_finished'] is not None): xml_resource.add_node("{0} upnp:recordedEndDateTime".format(xml_node_path), Basics.get_iso8601_datetime(entry_data['time_finished']))
		#
	#

	def _filter_metadata_of_didl_xml_node(self, xml_resource, xml_node_path):
	#
		"""
Uses the given XML resource to remove DIDL metadata not requested by the
client.

:param xml_resource: XML resource
:param xml_base_path: UPnP resource XML base path (e.g. "DIDL-Lite
                      item")

:since:  v0.1.00
		"""

		MpEntryVideo._filter_metadata_of_didl_xml_node(self, xml_resource, xml_node_path)

		if (self.get_type() & MpEntryPvrRecording.TYPE_CDS_ITEM == MpEntryPvrRecording.TYPE_CDS_ITEM and xml_resource.get_node(xml_node_path) is not None):
		#
			didl_fields = self.get_didl_fields()

			if (len(didl_fields) > 0):
			#
				if ("upnp:callSign" not in didl_fields): xml_resource.remove_node("{0} upnp:callSign".format(xml_node_path))
				if ("upnp:longDescription" not in didl_fields): xml_resource.remove_node("{0} upnp:longDescription".format(xml_node_path))
				if ("upnp:recordedStartDateTime" not in didl_fields): xml_resource.remove_node("{0} upnp:recordedStartDateTime".format(xml_node_path))
				if ("upnp:recordedEndDateTime" not in didl_fields): xml_resource.remove_node("{0} upnp:recordedEndDateTime".format(xml_node_path))
			#
		#
	#

	get_recording_status = MpEntryVideo._wrap_getter("recording_status")

	def get_type(self):
	#
		"""
Returns the UPnP resource type.

:return: (str) UPnP resource type; None if empty
:since:  v0.1.00
		"""

		_return = self.type

		if (_return is None):
		#
			entry_data = self.get_data_attributes("vfs_type")

			if (entry_data['vfs_type'] == MpEntryPvrRecording.VFS_TYPE_ITEM):
			#
				_return = (MpEntryPvrRecording.TYPE_CDS_ITEM
				           | MpEntryPvrRecording.TYPE_CDS_ITEM_PVR_VIDEO
				           | MpEntryPvrRecording.TYPE_CDS_ITEM_VIDEO
				          )

				_return = self._get_custom_type(_return)
			#
		#

		if (_return is None): _return = MpEntryVideo.get_type(self)

		return _return
	#

	def get_type_class(self):
	#
		"""
Returns the UPnP resource type class.

:return: (str) UPnP resource type class; None if unknown
:since:  v0.1.00
		"""

		_return = None

		is_cds2_container_supported = False
		_type = self.get_type()

		if (_type is not None):
		#
			client_settings = self.get_client_settings()
			is_cds2_container_supported = client_settings.get("upnp_didl_cds2_container_classes_supported", True)
		#

		if (is_cds2_container_supported
		    and _type & MpEntryPvrRecording.TYPE_CDS_ITEM_PVR_VIDEO == MpEntryPvrRecording.TYPE_CDS_ITEM_PVR_VIDEO
		   ): _return = "object.item.epgItem.videoProgram"

		if (_return is None): _return = MpEntryVideo.get_type_class(self)
		return _return
	#

	def set_data_attributes(self, **kwargs):
	#
		"""
Sets values given as keyword arguments to this method.

:since: v0.1.00
		"""

		with self:
		#
			MpEntryVideo.set_data_attributes(self, **kwargs)

			if ("channel" in kwargs): self.local.db_instance.channel = Binary.utf8(kwargs['channel'])
			if ("recording_status" in kwargs): self.local.db_instance.recording_status = kwargs['recording_status']
			if ("summary" in kwargs): self.local.db_instance.summary = Binary.utf8(kwargs['summary'])
			if ("time_started" in kwargs): self.local.db_instance.time_started = kwargs['time_started']
			if ("time_finished" in kwargs): self.local.db_instance.time_finished = kwargs['time_finished']
			if ("recorder" in kwargs): self.local.db_instance.recorder = Binary.utf8(kwargs['recorder'])
		#
	#

	set_recording_status = MpEntryVideo._wrap_setter("recording_status")
#

##j## EOF