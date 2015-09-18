# encoding: utf-8

from ..util import dprint, Context


@Context.register
class Iterator:
	priority = 50
	
	def match(self, context, line):
		return line.kind == 'code' and line.stripped.startswith("for ") and " in " in line.line
	
	def __call__(self, context):
		input = context.input
		
		if __debug__: dprint("\x1b[33;1m", "+", "Iterator", "\x1b[0m")
		
		declaration = input.next()
		yield declaration.clone(line=declaration.stripped + ':')
		
		context.scope += 1
		yield from context.stream
		context.scope -= 1
		
		if __debug__: dprint("\x1b[33m", "-", "Iterator", "\x1b[0m")
