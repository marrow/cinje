# encoding: utf-8

from ..util import ensure_buffer


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
		
		yield declaration.clone(line="__w(" + name.rstrip() + "(" + args.lstrip() + "))")
		
		context.flag.add('dirty')
