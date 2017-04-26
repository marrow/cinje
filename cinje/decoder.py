# encoding: utf-8

from __future__ import unicode_literals

from marrow.dsl.decoder import GalfiDecoder


class CinjeDecoder(GalfiDecoder):
	__slots__ = (
			'_flags',  # allow flags to be defined
			
			# additional options
		)
	
	EXTENSIONS = {  # mapping of joined Path.suffixes to the fully qualified encoding to interpret them using
			'.cinje': 'cinje',
			'.pyhtml': 'cinje.ns-html',
			'.pyxml': 'cinje.ns-xml',
		}
	
	FLAGS = {
			'free',  # ensure no runtime dependency on cinje
			'nomap',  # do not emit line number mappings
			'raw',  # make no effort to sanitize output; implies free
			'unbuffered',  # do not construct buffers and instead yield fragments as generated
			'wsgi',  # generate WSGI compatible template functions; incompatible with unbuffered and free
		}
