# encoding: utf-8

import codecs

from functools import partial
from encodings import utf_8 as utf8
from contextlib import contextmanager, _GeneratorContextManager

from .util import Context


def transform(input):
	translator = Context(input)
	return '\n'.join(str(i) for i in translator.stream)


def cinje_decode(input, errors='strict'):
	a = len(input)
	
	if hasattr(input, 'tobytes'):
		input = input.tobytes()
	
	if hasattr(input, 'decode'):
		input = input.decode('utf8', errors)
	
	return transform(input), a


class CinjeIncrementalDecoder(utf8.IncrementalDecoder):
	def decode(self, input, final=False):
		self.buffer += input
		
		if final:
			buff = self.buffer
			self.buffer = b''
			return super(CinjeIncrementalDecoder, self).decode(transform(buff).encode('utf8'), final=True)
		
		return ''


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
			incrementalencoder = utf8.IncrementalEncoder,
			incrementaldecoder = CinjeIncrementalDecoder,
			streamreader = CinjeStreamReader,
			streamwriter = utf8.StreamWriter
		)


codecs.register(cinje_search_function)
