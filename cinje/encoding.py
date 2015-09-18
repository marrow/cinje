# encoding: utf-8

import codecs

from functools import partial
from encodings import utf_8 as utf8
from contextlib import contextmanager, _GeneratorContextManager

from .util import Context


def transform(input):
	#__import__('pprint').pprint(input)
	translator = Context(input)
	return '\n'.join(str(i) for i in translator.stream)


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
