# encoding: utf-8

from __future__ import unicode_literals

from cinje.inline.comment import Comment


class TestInlineComment(object):
	def test_comment_passthrough(self):
		assert 'Hello world!' in b': def foo\n\t# Hello world!'.decode('cinje')
	
	def test_comment_muted(self):
		assert 'Hello world!' not in b': def foo\n\t## Hello world!'.decode('cinje')
