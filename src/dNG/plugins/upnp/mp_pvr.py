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

# pylint: disable=unused-argument

from dNG.data.upnp.resources.mp_entry_pvr_container import MpEntryPvrContainer
from dNG.database.condition_definition import ConditionDefinition
from dNG.plugins.hook import Hook
from dNG.runtime.exception_log_trap import ExceptionLogTrap
from dNG.runtime.value_exception import ValueException

def apply_value_derived_db_condition(params, last_return = None):
#
	"""
Called for "mp.upnp.MpResource.applyValueDerivedDbCondition"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
	"""

	if ("condition_definition" not in params
	    or "value" not in params
	   ): raise ValueException("Missing required arguments")

	condition_definition = params['condition_definition']
	value = "{0}.".format(params['value'])

	is_generic_container = "object.container.".startswith(value)
	is_video_container = "object.container.genre.movieGenre.".startswith(value)

	if (is_generic_container or is_video_container):
	#
		and_condition_definition = ConditionDefinition(ConditionDefinition.AND)

		and_condition_definition.add_exact_match_condition("cds_type", MpEntryPvrContainer.DB_CDS_TYPE_CONTAINER)
		and_condition_definition.add_exact_match_condition("identity", "MpUpnpPvrContainerResource")

		condition_definition.add_sub_condition(and_condition_definition)
	#

	return last_return
#

def on_control_point_shutdown(params, last_return = None):
#
	"""
Called for "dNG.pas.upnp.ControlPoint.onShutdown"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:since: v0.1.00
	"""

	pvr_managers = Hook.call("mp.pvr.Manager.getSingletons")

	if (type(pvr_managers) is list):
	#
		for pvr_manager in pvr_managers:
		#
			with ExceptionLogTrap("mp_pvr"): pvr_manager.stop()
		#
	#

	return last_return
#

def on_control_point_startup(params, last_return = None):
#
	"""
Called for "dNG.pas.upnp.ControlPoint.onStartup"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:since: v0.1.00
	"""

	pvr_managers = Hook.call("mp.pvr.Manager.getSingletons")

	if (type(pvr_managers) is list):
	#
		for pvr_manager in pvr_managers:
		#
			with ExceptionLogTrap("mp_pvr"): pvr_manager.start()
		#
	#

	return last_return
#

def register_plugin():
#
	"""
Register plugin hooks.

:since: v0.1.00
	"""

	Hook.register("dNG.pas.upnp.ControlPoint.onShutdown", on_control_point_shutdown)
	Hook.register("dNG.pas.upnp.ControlPoint.onStartup", on_control_point_startup)

	Hook.register("mp.upnp.MpResource.applyValueDerivedDbCondition", apply_value_derived_db_condition)
#

def unregister_plugin():
#
	"""
Unregister plugin hooks.

:since: v0.1.00
	"""

	Hook.unregister("dNG.pas.upnp.ControlPoint.onShutdown", on_control_point_shutdown)
	Hook.unregister("dNG.pas.upnp.ControlPoint.onStartup", on_control_point_startup)

	Hook.unregister("mp.upnp.MpResource.applyValueDerivedDbCondition", apply_value_derived_db_condition)
#

##j## EOF