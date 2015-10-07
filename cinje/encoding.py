# encoding: utf-8

from __future__ import unicode_literals

import codecs

from encodings import utf_8 as utf8

try:
	from io import StringIO
except:  # pragma: no cover
	try:
		from cStringIO import StringIO
	except:
		from StringIO import StringIO

from .util import Context

try:
	bytes = bytes
except:  # pragma: no cover
	bytes = str

try:
	unicode = unicode
except:  # pragma: no cover
	unicode = str


def transform(input):
	#__import__('pudb').set_trace()
	translator = Context(input)
	return '\n'.join(unicode(i) for i in translator.stream)


def cinje_decode(input, errors='strict', final=True):
	if not final: return '', 0
	output = transform(bytes(input).decode('utf8', errors))
	return output, len(input)


class CinjeIncrementalDecoder(utf8.IncrementalDecoder):
	def _buffer_decode(self, input, errors='strict', final=False):
		if not final or len(input) == 0:
			return '', 0
		
		output = transform(bytes(input).decode('utf8', errors))
		
		return output, len(input)


class CinjeStreamReader(utf8.StreamReader):
	def __init__(self, *args, **kw):
		codecs.StreamReader.__init__(self, *args, **kw)
		self.stream = StringIO(transform(self.stream))


def cinje_search_function(name):
	if name != 'cinje':
		return None
	
	return codecs.CodecInfo(
			name = 'cinje',
			encode = utf8.encode,
			decode = cinje_decode,
			incrementalencoder = None, # utf8.IncrementalEncoder,
			incrementaldecoder = CinjeIncrementalDecoder, # utf8.IncrementalDecoder,
			streamreader = CinjeStreamReader,
			streamwriter = utf8.StreamWriter
		)


codecs.register(cinje_search_function)
