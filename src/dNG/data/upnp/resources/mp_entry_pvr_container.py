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

from sqlalchemy.sql.expression import and_

from dNG.database.connection import Connection
from dNG.database.instances.mp_upnp_pvr_container_resource import MpUpnpPvrContainerResource as _DbMpUpnpPvrContainerResource
from dNG.database.instances.mp_upnp_pvr_recording_resource import MpUpnpPvrRecordingResource as _DbMpUpnpPvrRecordingResource
from dNG.database.nothing_matched_exception import NothingMatchedException
from dNG.database.sort_definition import SortDefinition

from .mp_entry import MpEntry

class MpEntryPvrContainer(MpEntry):
    """
"MpEntryPvrContainer" is used for UPnP PVR container database entries.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    mp
:subpackage: pvr
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
    """

    _DB_INSTANCE_CLASS = _DbMpUpnpPvrContainerResource
    """
SQLAlchemy database instance class to initialize for new instances.
    """
    TYPE_CDS_CONTAINER_PVR_VIDEO = 1 << 32
    """
UPnP CDS PVR video container type
    """

    def __init__(self, db_instance = None, user_agent = None, didl_fields = None):
        """
Constructor __init__(MpEntry)

:param db_instance: Encapsulated SQLAlchemy database instance
:param user_agent: Client user agent
:param didl_fields: DIDL fields list

:since: v0.1.00
        """

        MpEntry.__init__(self, db_instance, user_agent, didl_fields)

        self.supported_features['content_list_where_condition'] = self._supports_content_list_where_condition
        self.supported_features['auto_maintenance'] = True
    #

    def _apply_content_list_where_condition(self, db_query):
        """
Returns the modified SQLAlchemy database query with the "where" condition
applied.

:param db_query: Unmodified SQLAlchemy database query

:return: (object) SQLAlchemy database query
:since:  v0.1.00
        """

        _return = db_query

        client_settings = self.get_client_settings()

        if (self.type & MpEntryPvrContainer.TYPE_CDS_CONTAINER_PVR_VIDEO == MpEntryPvrContainer.TYPE_CDS_CONTAINER_PVR_VIDEO
            and (client_settings.get("upnp_pvr_scheduled_recording_supported", True))
           ):
            _return = _return.filter(and_(_DbMpUpnpPvrContainerResource.identity == "MpUpnpPvrRecordingResource",
                                          _DbMpUpnpPvrRecordingResource.mimeclass != "unknown"
                                         )
                                    )
        #

        return _return
    #

    def _get_default_sort_definition(self, context = None):
        """
Returns the default sort definition list.

:param context: Sort definition context

:return: (object) Sort definition
:since:  v0.1.00
        """

        if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._get_default_sort_definition({1})- (#echo(__LINE__)#)", self, context, context = "pas_datalinker")

        return (SortDefinition([ ( "vfs_type", SortDefinition.ASCENDING ),
                                 ( "position", SortDefinition.ASCENDING ),
                                 ( "time_sortable", SortDefinition.ASCENDING ),
                                 ( "resource_title", SortDefinition.ASCENDING )
                               ])
                if (context == "MpEntry") else
                MpEntry._get_default_sort_definition(self, context)
               )
    #

    def get_type(self):
        """
Returns the UPnP resource type.

:return: (str) UPnP resource type; None if empty
:since:  v0.1.00
        """

        _return = self.type

        if (_return is None):
            entry_data = self.get_data_attributes("vfs_type")

            if (entry_data['vfs_type'] == MpEntryPvrContainer.VFS_TYPE_DIRECTORY
                and self.get_mimetype() == "text/x-directory-upnp-pvr-video"
               ):
                _return = (MpEntryPvrContainer.TYPE_CDS_CONTAINER
                           | MpEntryPvrContainer.TYPE_CDS_CONTAINER_PVR_VIDEO
                           | MpEntryPvrContainer.TYPE_CDS_CONTAINER_VIDEO
                          )

                _return = self._get_custom_type(_return)
            #
        #

        if (_return is None): _return = MpEntry.get_type(self)

        return _return
    #

    def get_type_class(self):
        """
Returns the UPnP resource type class.

:return: (str) UPnP resource type class; None if unknown
:since:  v0.1.00
        """

        _return = None

        is_cds2_container_supported = False
        _type = self.get_type()

        if (_type is not None):
            client_settings = self.get_client_settings()
            is_cds2_container_supported = client_settings.get("upnp_didl_cds2_container_classes_supported", True)
        #

        if (is_cds2_container_supported
            and _type & MpEntryPvrContainer.TYPE_CDS_CONTAINER_PVR_VIDEO == MpEntryPvrContainer.TYPE_CDS_CONTAINER_PVR_VIDEO
           ): _return = "object.container.epgContainer"

        if (_return is None): _return = MpEntry.get_type_class(self)
        return _return
    #

    def save(self):
        """
Saves changes of the database task instance.

:since: v0.1.00
        """

        with self:
            if (self.local.db_instance.mimeclass is None): self.local.db_instance.mimeclass = "directory"
            if (self.local.db_instance.mimetype is None): self.local.db_instance.mimetype = "text/x-directory-upnp-pvr-video"

            MpEntry.save(self)
        #
    #

    def set_data_attributes(self, **kwargs):
        """
Sets values given as keyword arguments to this method.

:since: v0.1.00
        """

        with self:
            MpEntry.set_data_attributes(self, **kwargs)
            if ("manager_id" in kwargs): self.local.db_instance.manager_id = kwargs['manager_id']
        #
    #

    def _supports_content_list_where_condition(self):
        """
Returns true if the SQLAlchemy database query "where" condition for the
resource's content list is modified.

:return: (bool) True if resource content list condition is modified.
:since:  v0.1.00
        """

        client_settings = self.get_client_settings()

        return (self.get_type() & MpEntryPvrContainer.TYPE_CDS_CONTAINER_PVR_VIDEO == MpEntryPvrContainer.TYPE_CDS_CONTAINER_PVR_VIDEO
                and (client_settings.get("upnp_pvr_scheduled_recording_supported", True))
               )
    #

    @classmethod
    def load_manager_root_container(cls, manager_id, client_user_agent = None, cds = None, deleted = False):
        """
Loads the root container of the given PVR manager ID.

:param cls: Expected encapsulating database instance class
:param manager_id: UPnP CDS ID
:param client_user_agent: Client user agent
:param cds: UPnP CDS
:param deleted: True to include deleted resources

:return: (object) Resource object; None on error
:since:  v0.1.00
        """

        if (manager_id is None): raise NothingMatchedException("PVR manager ID is invalid")

        with Connection.get_instance() as connection:
            db_instance = (connection.query(_DbMpUpnpPvrContainerResource)
                           .filter(_DbMpUpnpPvrContainerResource.role_id == "upnp_root_container",
                                   _DbMpUpnpPvrContainerResource.manager_id == manager_id
                                  )
                           .first()
                          )

            if (db_instance is None): raise NothingMatchedException("PVR manager ID '{0}' is invalid".format(manager_id))
            MpEntry._ensure_db_class(cls, db_instance)

            return MpEntryPvrContainer(db_instance)
        #
    #
#
