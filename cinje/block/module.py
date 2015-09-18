# encoding: utf-8

from ..util import dprint, Line, Context


@Context.register
class Module:
	"""Module handler.
	
	This is the initial scope, and the highest priority to ensure its processing of the preamble happens first.
	"""
	
	priority = -100
	
	def match(self, context, line):
		return 'init' not in context.flag
	
	def __call__(self, context):
		input = context.input
		
		context.flag.add('init')
		if __debug__: dprint("\x1b[33;1m", "+", "Module", "\x1b[0m")
		
		imported = False
		
		for line in input:
			if not line.stripped or line.stripped[0] == '#':
				if not line.stripped.startswith('##'):
					yield line
				continue
			
			input.push(line)  # We're out of the preamble, so put that line back and stop.
			break
		
		# After any existing preamble, but before other imports, we inject our own.
		yield Line(0, 'import cinje')  
		yield Line(0, '')
		yield Line(0, 'from cinje.helpers import escape as _escape, bless as _bless, iterate, xmlargs as _args, _interrupt')
		yield Line(0, '')
		
		yield from context.stream  # This increases the scope.
		
		context.flag.remove('init')
		if __debug__: dprint("\x1b[33m", "-", "Module", "\x1b[0m")
