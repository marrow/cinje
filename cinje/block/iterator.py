# encoding: utf-8

from ..util import Context


@Context.register
class Iterator(object):
	priority = 50
	
	def match(self, context, line):
		return line.kind == 'code' and line.stripped.startswith("for ") and " in " in line.line
	
	def __call__(self, context):
		input = context.input
		
		declaration = input.next()
		yield declaration.clone(line=declaration.stripped + ':')
		
		context.scope += 1
		
		for i in context.stream:
			yield i
		
		context.scope -= 1
