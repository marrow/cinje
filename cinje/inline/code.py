# encoding: utf-8


class Code(object):
	"""General code handler.
	
	This captures all code segments not otherwise handled.  It has a very low priority to ensure other "code" handlers
	get a chance to run first.
	
	Syntax:
	
		: <code>
	"""
	
	priority = 100
	
	def match(self, context, line):
		return line.kind == 'code'
	
	def __call__(self, context):
		yield context.input.next()  # Pass through.
