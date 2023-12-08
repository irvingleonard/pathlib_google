#!python
'''Pathlib implementation for Google Drive
Implements PurePath and Path classes for Google Drive.
'''

import logging

from pathlib_._base import BasePath, BasePurePath

LOGGER = logging.getLogger(__name__)


class PureGoogleDrivePath(BasePurePath):
	'''Pure Google Drive path
	There's not really a path convention in Google Drive afaik: the content (file/folders) is addressed by ID. There's still a classic tree-like construct that's shown to the users of the interface which derives from the fact that entries have parents, hence a tree based on the "drive root" (actual existing concept).

	This path format is then not applicable to anything Google Drive related outside this module, but should be good enough for most cases. The convention is as follows:
	- the "/" character is assumed to be the separator. Folder/files/drives with "/" in the name will break this (Google Drive will hapily create such content).
	- there's the concept of "Shared Drives" which comes to be similar of how "drives" work in Windows. A set of double separators '//' at the beginning of the path signals the use of drives, and the name will be assumed as everything until the next ocurrence of "//". A set of "//" anywhere else on the path would only yield an empty part. A drive with "//" in the name will break this convention, and Google won't limit such name.
	'''

	DRIVE_SUPPORTED = True

	@classmethod
	def _parse_path(cls, path):
		'''Local parsing logic
		Should implement whatever logic is needed to parse the provided path string into a tuple (drive, root, tail)

		Drive and/or root could be empty, but both should be strings. Tail should be a sequence (could be empty too).
		The empty path would yield ('', '', [])

		The method should not try to simplify the path (resolve globbing, remove separator repetitions, etc.). The class must be able to recreate the original values, which becomes impossible if any part of it is removed here.
		'''

		if path:
			if path[0] == cls.SEPARATOR:
				if path[1:2] == cls.SEPARATOR:
					drive = path[2:path[2:].find('//') + 2]
					root = cls.SEPARATOR
					tail = path[len(drive) + 4]
				else:
					drive = ''
					root = cls.SEPARATOR
					tail = path[1:]
			else:
				drive, root = '', ''
				tail = path
			tail = tail.split(cls.SEPARATOR) if tail else []
			return (drive, root, tail)
		else:
			return ('', '', [])


class GoogleDrivePath(BasePath, PureGoogleDrivePath):

	def __new__(cls, *args, drive = None, root = None, tail = None, client = None):

		if client is None:
			raise ValueError('Need to provide a Google Drive client for real paths. Check the "from_credentials()" method')

	@classmethod
	def new_instance(cls, *args, **kwargs):
		a = cls(*args, **kwargs)
		return a.parts, a[:], str(a)
