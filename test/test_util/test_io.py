# encoding: utf-8

from __future__ import unicode_literals

from io import StringIO, BytesIO

from cinje import flatten, fragment

tmpl = fragment("Zoë")


class TestCinjeIO(object):
	def test_flatten_string_unicode(self):
		assert flatten(tmpl()) == 'Zoë\n'
	
	def test_flatten_string_binary(self):
		assert flatten(tmpl(), encoding='utf8') == 'Zoë\n'.encode('utf8')
	
	def test_flatten_filelike_unicode(self):
		container = StringIO()
		assert flatten(tmpl(), container) == 4
		assert container.getvalue() == 'Zoë\n'
	
	def test_flatten_filelike_binary(self):
		container = BytesIO()
		assert flatten(tmpl(), container, encoding='utf8') == 5
		assert container.getvalue() == 'Zoë\n'.encode('utf8')
