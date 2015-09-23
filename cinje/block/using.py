# encoding: utf-8

from ..util import dprint, Line, Context, ensure_buffer


@Context.register
class Using:
	priority = 25
	
	def match(self, context, line):
		return line.kind == 'code' and line.stripped.startswith("using ")
	
	def __call__(self, context):
		input = context.input
		
		if __debug__: dprint("\x1b[33;1m", "+", "Using", "\x1b[0m")
		
		declaration = _declaration = input.next()
		
		_, _, declaration = declaration.stripped.partition(' ')
		name, _, args = declaration.partition(' ')
		
		name = name.strip()
		args = args.strip()
		
		if 'using' not in context.flag:
			context.flag.add('using')
			yield Line(0, "_using_stack = []")
		
		yield from ensure_buffer(context)
		
		yield Line(0, "_using_stack.append(" + name + "(" + args + "))")
		yield Line(0, "_buffer.extend(_interrupt(_using_stack[-1]))")
		
		context.flag.add('dirty')
			
		yield from context.stream
		
		yield Line(0, "_buffer.extend(_using_stack.pop())")
		
		context.flag.add('dirty')
		
		if __debug__: dprint("\x1b[33m", "-", "Using", "\x1b[0m")
