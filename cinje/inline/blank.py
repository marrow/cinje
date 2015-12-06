# encoding: utf-8


class Blank(object):
	"""Blank line handler.  This eats leading blank lines."""
	
	priority = -90
	
	def match(self, context, line):
		return not line.stripped
	
	def __call__(self, context):
		yield context.input.next()
