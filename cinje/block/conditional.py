# encoding: utf-8

from ..util import dprint, Line, Context


@Context.register
class Conditional:
	"""Conditional template evaluation support.  Blocks must be terminated by ": end" markers.
	
	This block-level transformer handles "if", "elif", and "else" conditional scopes.
	
	Syntax::
	
		: if <expression>
		: elif <expression>
		: else
		: end
	
	Single-line conditionals are not allowed, and the declaration should not include a trailing colon.
	"""
	
	priority = 50
	
	def match(self, context, line):
		"""Match code lines prefixed with an "if", "elif", or "else" keyword."""
		
		return line.kind == 'code' and line.partitioned[0] in ('if', 'else', 'elif')
	
	def __call__(self, context):
		"""Process conditional declarations."""
		
		input = context.input
		
		if __debug__: dprint("\x1b[33;1m", "+", "Conditional", "\x1b[0m")
		
		declaration = input.next()
		stripped = declaration.stripped
		prefix, _ = declaration.partitioned
		
		if prefix != 'if':  # We're handling an alternate section…
			context.scope -= 1  # Reduce the scope temporarily to emit the new declaration.
			yield declaration.clone(line=stripped + ':')
			context.scope += 1
			return  # We'll bounce back to the "if" Conditional instance.
		
		yield declaration.clone(line=stripped + ':')
		
		context.scope += 1
		
		yield from context.stream
		
		context.scope -= 1
		
		if __debug__: dprint("\x1b[33m", "-", "Conditional", "\x1b[0m")
