# encoding: utf-8

from __future__ import unicode_literals

from marrow.dsl.decoder import GalfiDecoder


class CinjeDecoder(GalfiDecoder):
	__slots__ = ('_flags')
	
	FLAGS = {
		}
