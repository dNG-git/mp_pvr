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

from dNG.data.upnp.resources.mp_entry_pvr_container import MpEntryPvrContainer
from dNG.database.connection import Connection
from dNG.database.nothing_matched_exception import NothingMatchedException
from dNG.database.transaction_context import TransactionContext
from dNG.module.named_loader import NamedLoader
from dNG.runtime.instance_lock import InstanceLock
from dNG.runtime.not_implemented_exception import NotImplementedException
from dNG.runtime.thread_lock import ThreadLock
from dNG.runtime.value_exception import ValueException

class AbstractManager(object):
#
	"""
"AbstractManager" defines abstract methods to implement a PVR manager.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    mp
:subpackage: pvr
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	id = None
	"""
PVR manager identifier
	"""
	_instance_lock = InstanceLock()
	"""
Thread safety lock
	"""
	_weakref_instance = None
	"""
PVR manager weakref instance
	"""

	def __init__(self):
	#
		"""
Constructor __init__(AbstractManager)

:since: v0.1.00
		"""

		self._lock = ThreadLock()
		"""
Thread safety lock
		"""
		self.log_handler = NamedLoader.get_singleton("dNG.data.logging.LogHandler", False)
		"""
The LogHandler is called whenever debug messages should be logged or errors
happened.
		"""
		self.name = None
		"""
PVR manager instance name
		"""
		self.root_container = None
		"""
Cached UPnP PVR root container instance
		"""
	#

	@Connection.wrap_callable
	def _ensure_root_container(self):
	#
		"""
Returns the PVR container holding recordings.

:return: (object) UPnP PVR container resource
:since:  v0.1.00
		"""

		if (self.root_container is None):
		#
			with self._lock:
			# Thread safety
				if (self.root_container is None):
				#
					try: self.root_container = MpEntryPvrContainer.load_manager_root_container(self.get_manager_id())
					except NothingMatchedException:
					#
						container = MpEntryPvrContainer()
						name = self.get_name()

						container_data = { "title": name,
						                   "vfs_url": "{0}:///".format(self.get_vfs_scheme()),
						                   "vfs_type": MpEntryPvrContainer.VFS_TYPE_DIRECTORY,
						                   "role_id": "upnp_root_container",
						                   "resource_title": name,
						                   "manager_id": self.get_manager_id()
						                 }

						container.set_data_attributes(**container_data)
						container.set_as_main_entry()
						container.save()

						self.root_container = container
					#
				#
			#
		#
	#

	def get_container(self):
	#
		"""
Returns the PVR container holding recordings.

:return: (object) UPnP PVR container resource
:since:  v0.1.00
		"""

		self._ensure_root_container()
		return self.root_container
	#

	def get_manager_id(self):
	#
		"""
Returns the PVR manager identifier.

:return: (str) PVR manager identifier
:since:  v0.1.00
		"""

		if (self.__class__.id is None): raise ValueException("The PVR manager instance is invalid")
		return self.__class__.id
	#

	def get_name(self):
	#
		"""
Returns the PVR manager instance name.

:return: (str) PVR manager instance name
:since:  v0.1.00
		"""

		if (self.name is None): raise ValueException("The PVR manager instance is invalid")
		return self.name
	#

	def get_vfs_scheme(self):
	#
		"""
Returns the PVR manager VFS scheme.

:return: (str) PVR manager VFS scheme
:since:  v0.1.00
		"""

		return "x-{0}".format(NamedLoader.RE_CAMEL_CASE_SPLITTER
		                      .sub("\\1-\\2", self.get_manager_id())
		                      .lower()
		                     )
	#

	def start(self, params = None, last_return = None):
	#
		"""
Starts the activity of this manager.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
		"""

		self._ensure_root_container()

		return last_return
	#

	def stop(self, params = None, last_return = None):
	#
		"""
Stops the activity of this manager.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
		"""

		return last_return
	#

	@staticmethod
	def get_instance():
	#
		"""
Get the PVR manager singleton.

:return: (object) PVR manager instance on success
:since:  v0.1.00
		"""

		raise NotImplementedException()
	#
#

##j## EOF