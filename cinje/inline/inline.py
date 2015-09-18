# encoding: utf-8

from ..util import dprint, Line, Context


@Context.register
class Inline:
	priority = 25
	
	def match(self, context, line):
		return line.kind == 'code' and line.stripped == "yield"  # Bare yields indicate insertion points.
	
	def __call__(self, context):
		input = context.input
		
		if __debug__: dprint("\x1b[34m", "?", "Inline", "\x1b[0m")
		
		if 'dirty' in context.flag:
			yield Line(0, 'yield "".join(_buffer); _buffer.clear()')
			context.flag.remove('dirty')
		
		yield input.next()
