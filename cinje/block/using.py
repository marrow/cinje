# encoding: utf-8

from ..util import Line, ensure_buffer


class Using(object):
	priority = 25
	
	def match(self, context, line):
		return line.kind == 'code' and line.stripped.startswith("using ")
	
	def __call__(self, context):
		input = context.input
		
		declaration = input.next()
		
		_, _, declaration = declaration.stripped.partition(' ')
		name, _, args = declaration.partition(' ')
		
		name = name.strip()
		args = args.strip()
		
		if 'using' not in context.flag:
			context.flag.add('using')
			yield Line(0, "_using_stack = []")
		
		for i in ensure_buffer(context):
			yield i
		
		yield Line(0, "_using_stack.append(" + name + "(" + args + "))")
		yield Line(0, "_buffer.extend(_interrupt(_using_stack[-1]))")
		
		context.flag.add('dirty')
		
		for i in context.stream:
			yield i
		
		yield Line(0, "_buffer.extend(_using_stack.pop())")
		
		context.flag.add('dirty')
