# encoding: utf-8

from __future__ import unicode_literals

from cinje.util import py, Context
from cinje.block.module import Module
from cinje.inline.code import Code


class TestContextBehaviours(object):
	def test_repr_is_reasonable(self):
		context = Context('')
		
		if py == 2:
			assert repr(context) == 'Context(Lines(1), 0, set([]))'
		else:
			assert repr(context) == 'Context(Lines(1), 0, set())'
	
	def test_prepare_required_translator_priority(self):
		context = Context('')
		context.prepare()
		assert isinstance(context._handler[0], Module), "Module must be first priority."
		assert isinstance(context._handler[-1], Code), "Code must be last priority."
	
	def test_first_handler(self):
		context = Context('')
		context.prepare()
		assert context.classify(": foo") is context._handler[0]
