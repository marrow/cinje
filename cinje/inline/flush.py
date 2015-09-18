# encoding: utf-8

from ..util import dprint, Context


@Context.register
class Flush:
	priority = 25
	
	def match(self, context, line):
		return line.kind == 'code' and line.stripped == "flush"
	
	def __call__(self, context):
		input = context.input
		
		if __debug__: dprint("\x1b[34m", "?", "Flush", "\x1b[0m")
		
		assert 'text' in context.flag, "Without preceeding content unexpected flush is unexpected." 
		
		declaration = input.next()
		yield declaration.clone(line='yield "".join(_buffer); _buffer.clear()')
		
		if 'dirty' in context.flag:
			context.flag.remove('dirty')
