# encoding: utf-8

from __future__ import unicode_literals

from cinje.util import str, Pipe


class TestPipeBehaviour(object):
	def test_basic_usage(self):
		@Pipe
		def text(value):
			return str(value)
		
		assert (27 | text) == "27"
	
	def test_repr_is_reasonable(self):
		@Pipe
		def text(value):
			return str(value)
		
		assert repr(text).startswith('Pipe(<function')
		assert 'text' in repr(text)
	
	def test_argument_specialization(self):
		@Pipe
		def encode(value, encoding='utf8'):
			return str(value).encode(encoding)
		
		utf8 = encode(encoding='utf8')
		latin1 = encode(encoding='latin1')
		
		assert ("Zoë" | utf8) == b'Zo\xc3\xab'
		assert ("Zoë" | latin1) == b'Zo\xeb'
