# encoding: utf-8

from ..util import py, pypy, ensure_buffer

PREFIX = '_buffer.extend(' if pypy else '__w(' 


class Use(object):
	"""Consume the result of calling another template function, extending the local buffer.
	
	This is meant to consume non-wrapping template functions.  For wrapping functions see ": using" instead.
	
	Syntax:
	
		: use <name-constant> [<arguments>]
	
	The name constant must resolve to a generator function that participates in the cinje "yielded buffer" protocol.
	
	"""
	
	priority = 25
	
	def match(self, context, line):
		"""Match code lines prefixed with a "use" keyword."""
		return line.kind == 'code' and line.partitioned[0] == "use"
	
	def __call__(self, context):
		"""Wrap the expression in a `_buffer.extend()` call."""
		
		input = context.input
		
		declaration = input.next()
		parts = declaration.partitioned[1]  # Ignore the "use" part, we care about the name and arguments.
		name, _, args = parts.partition(' ')
		
		for i in ensure_buffer(context):
			yield i
		
		name = name.rstrip()
		args = args.lstrip()
		
		if 'buffer' in context.flag:
			yield declaration.clone(line=PREFIX + name + "(" + args + "))")
			context.flag.add('dirty')
			return
		
		if py == 3:  # We can use the more efficient "yield from" syntax. Wewt!
			yield declaration.clone(line="yield from " + name + "(" + args + ")")
		else:
			yield declaration.clone(line="for _chunk in " + name + "(" + args + "):")
			yield declaration.clone(line="yield _chunk", scope=context.scope + 1)

