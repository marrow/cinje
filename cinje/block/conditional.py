# encoding: utf-8

from ..util import dprint, Line, Context


@Context.register
class Conditional:
	priority = 50
	
	def match(self, context, line):
		if line.kind != 'code':
			return
		
		prefix, _, _ = line.stripped.partition(' ')
		prefix = prefix.strip()
		
		return prefix in ('if', 'else', 'elif')
	
	def __call__(self, context):
		input = context.input
		
		if __debug__: dprint("\x1b[33;1m", "+", "Conditional", "\x1b[0m")
		
		declaration = input.next()
		
		prefix, _, _ = declaration.stripped.partition(' ')
		prefix = prefix.strip()
		
		if prefix != 'if':  # We're handling an alternate section…
			context.scope -= 1
			yield declaration.clone(line=declaration.stripped + ':')
			context.scope += 1
			return  # We'll bounce back to the "if" Conditional instance.
		
		yield declaration.clone(line=declaration.stripped + (':' if ':' not in declaration.stripped else ''))
		
		if ':' in declaration.stripped and declaration.stripped[-1] != ':':
			if __debug__: dprint("\x1b[33m", "-", "Conditional", "\x1b[0m")
			return
		
		context.scope += 1
		
		yield from context.stream
		
		context.scope -= 1
		
		if __debug__: dprint("\x1b[33m", "-", "Conditional", "\x1b[0m")
