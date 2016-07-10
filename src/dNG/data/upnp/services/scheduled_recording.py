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

from dNG.data.upnp.resource import Resource
from dNG.data.upnp.upnp_exception import UpnpException

from .abstract_service import AbstractService
from .feature_list_mixin import FeatureListMixin

_py_filter = filter
"""
Remapped filter builtin
"""

class ScheduledRecording(FeatureListMixin, AbstractService):
#
	"""
Implementation for "urn:schemas-upnp-org:service:ScheduledRecording:1".

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    mp
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	# pylint: disable=redefined-builtin,unused-argument

	def __init__(self):
	#
		"""
Constructor __init__(ScheduledRecording)

:since: v0.1.00
		"""

		AbstractService.__init__(self)
		FeatureListMixin.__init__(self)
	#

	def get_sort_capabilities(self):
	#
		"""
Returns the system-wide UPnP sort capabilities available.

:return: (int) UPnP sort capabilities value
:since:  v0.1.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.get_sort_capabilities()- (#echo(__LINE__)#)", self, context = "mp_server")
		_return = UpnpException("pas_http_core_404", 701)

		resource = Resource.load_cds_id("0", self.client_user_agent, self)
		if (resource is not None): _return = resource.get_sort_capabilities()

		return _return
	#

	def get_version(self):
	#
		"""
Returns the UPnP service type version.

:return: (str) Service type version
:since:  v0.1.00
		"""

		client_settings = self.get_client_settings()
		is_versioning_supported = client_settings.get("upnp_spec_versioning_supported", True)

		return (AbstractService.get_version(self) if (is_versioning_supported) else 1)
	#

	def init_host(self, device, service_id = None, configid = None):
	#
		"""
Initializes a host service.

:param device: Host device this UPnP service is added to
:param service_id: Unique UPnP service ID
:param configid: UPnP configId for the host device

:return: (bool) Returns true if initialization was successful.
:since:  v0.1.00
		"""

		self.type = "ScheduledRecording"
		self.upnp_domain = "schemas-upnp-org"
		self.version = "2"

		if (service_id is None): service_id = "ScheduledRecording"

		return AbstractService.init_host(self, device, service_id, configid)
	#

	def _init_host_actions(self, device):
	#
		"""
Initializes the dict of host service actions.

:param device: Host device this UPnP service is added to

:since: v0.1.00
		"""

		browse_record_schedules = { "argument_variables": [ { "name": "Filter", "variable": "A_ARG_TYPE_PropertyList" },
		                                                    { "name": "StartingIndex", "variable": "A_ARG_TYPE_Index" },
		                                                    { "name": "RequestedCount", "variable": "A_ARG_TYPE_Count" },
		                                                    { "name": "SortCriteria", "variable": "A_ARG_TYPE_SortCriteria" }
		                                                  ],
		                            "return_variable": { "name": "Result", "variable": "A_ARG_TYPE_RecordSchedule" },
		                            "result_variables": [ { "name": "NumberReturned", "variable": "A_ARG_TYPE_Count" },
		                                                  { "name": "TotalMatches", "variable": "A_ARG_TYPE_Count" },
		                                                  { "name": "UpdateID", "variable": "StateUpdateID" }
		                                                ]
		                          }

		browse_record_tasks = { "argument_variables": [ { "name": "RecordScheduleID", "variable": "A_ARG_TYPE_ObjectID" },
		                                                { "name": "Filter", "variable": "A_ARG_TYPE_PropertyList" },
		                                                { "name": "StartingIndex", "variable": "A_ARG_TYPE_Index" },
		                                                { "name": "RequestedCount", "variable": "A_ARG_TYPE_Count" },
		                                                { "name": "SortCriteria", "variable": "A_ARG_TYPE_SortCriteria" }
		                                              ],
		                        "return_variable": { "name": "Result", "variable": "A_ARG_TYPE_RecordTask" },
		                        "result_variables": [ { "name": "NumberReturned", "variable": "A_ARG_TYPE_Count" },
		                                              { "name": "TotalMatches", "variable": "A_ARG_TYPE_Count" },
		                                              { "name": "UpdateID", "variable": "StateUpdateID" }
		                                            ]
		                      }

		create_record_schedule = { "argument_variables": [ { "name": "Elements", "variable": "A_ARG_TYPE_RecordScheduleParts" } ],
		                           "return_variable": { "name": "RecordScheduleID", "variable": "A_ARG_TYPE_ObjectID" },
		                           "result_variables": [ { "name": "Result", "variable": "A_ARG_TYPE_RecordSchedule" },
		                                                 { "name": "UpdateID", "variable": "StateUpdateID" }
		                                               ]
		                         }

		get_default_values = { "argument_variables": [ { "name": "DataTypeID", "variable": "A_ARG_TYPE_DataTypeID" },
		                                               { "name": "Filter", "variable": "A_ARG_TYPE_PropertyList" }
		                                             ],
		                       "return_variable": { "name": "PropertyInfo", "variable": "A_ARG_TYPE_PropertyInfo" },
		                       "result_variables": [ ]
		                     }

		self.actions = { "GetAllowedValues": get_default_values,
		                 "BrowseRecordSchedules": browse_record_schedules,
		                 "BrowseRecordTasks": browse_record_tasks,
		                 "CreateRecordSchedule": create_record_schedule
		               }
	#

	def _init_host_variables(self, device):
	#
		"""
Initializes the dict of host service variables.

:param device: Host device this UPnP service is added to

:since: v0.1.00
		"""

		self.variables = { "SortCapabilities": { "is_sending_events": False,
		                                         "is_multicasting_events": False,
		                                         "type": "string"
		                                       },
		                   "SortLevelCapability": { "is_sending_events": False,
		                                            "is_multicasting_events": False,
		                                            "type": "ui4"
		                                          },
		                   "StateUpdateID": { "is_sending_events": False,
		                                      "is_multicasting_events": False,
		                                      "type": "ui4"
		                                    },
		                   "LastChange": { "is_sending_events": True,
		                                   "is_multicasting_events": False,
		                                   "type": "string"
		                                 },
		                   "A_ARG_TYPE_PropertyList": { "is_sending_events": False,
		                                                "is_multicasting_events": False,
		                                                "type": "string"
		                                              },
		                   "A_ARG_TYPE_DataTypeID": { "is_sending_events": False,
		                                              "is_multicasting_events": False,
		                                              "type": "string",
		                                              "values_allowed": [ "A_ARG_TYPE_RecordSchedule",
		                                                                  "A_ARG_TYPE_RecordTask",
		                                                                  "A_ARG_TYPE_RecordScheduleParts"
		                                                                ]
		                                            },
		                   "A_ARG_TYPE_ObjectID": { "is_sending_events": False,
		                                            "is_multicasting_events": False,
		                                            "type": "string"
		                                          },
		                   "A_ARG_TYPE_ObjectIDList": { "is_sending_events": False,
		                                                "is_multicasting_events": False,
		                                                "type": "string"
		                                              },
		                   "A_ARG_TYPE_PropertyInfo": { "is_sending_events": False,
		                                                "is_multicasting_events": False,
		                                                "type": "string"
		                                              },
		                   "A_ARG_TYPE_Index": { "is_sending_events": False,
		                                         "is_multicasting_events": False,
		                                         "type": "ui4"
		                                       },
		                   "A_ARG_TYPE_Count": { "is_sending_events": False,
		                                         "is_multicasting_events": False,
		                                         "type": "ui4"
		                                       },
		                   "A_ARG_TYPE_SortCriteria": { "is_sending_events": False,
		                                                "is_multicasting_events": False,
		                                                "type": "string"
		                                              },
		                   "A_ARG_TYPE_RecordSchedule": { "is_sending_events": False,
		                                                  "is_multicasting_events": False,
		                                                  "type": "string"
		                                                },
		                   "A_ARG_TYPE_RecordTask": { "is_sending_events": False,
		                                              "is_multicasting_events": False,
		                                              "type": "string"
		                                            },
		                   "A_ARG_TYPE_RecordScheduleParts": { "is_sending_events": False,
		                                                       "is_multicasting_events": False,
		                                                       "type": "string"
		                                                     }
		                 }
	#
#

##j## EOF