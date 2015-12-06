# encoding: utf-8

from __future__ import unicode_literals

from cinje.inline.comment import Comment


class TestInlineCode(object):
	def test_blank_eating(self):
		assert "'\\tEaten.\\n'" in b': def test\n\t\n\tEaten.'.decode('cinje')
	
	def test_code_fallback(self):
		assert 'arbitrary code' in b': arbitrary code'.decode('cinje')
