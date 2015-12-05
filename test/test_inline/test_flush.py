# encoding: utf-8

from __future__ import unicode_literals

from cinje.inline.flush import Flush


class TestInlineFlush(object):
	def test_non_template_function(self):
		assert 'yield' not in b': def test\n\t: pass'.decode('cinje')
	
	def test_natural_flush(self):
		assert b': def test\n\tHello.'.decode('cinje').count('yield') == 1
	
	def test_forced_omits_natural_flush(self):
		assert b': def test\n\tHello.\n\t: flush'.decode('cinje').count('yield') == 1
	
	def test_forced_and_natural_flush(self):
		assert b': def test\n\tHello.\n\t: flush\n\tWorld.'.decode('cinje').count('yield') == 2
