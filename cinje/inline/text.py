# encoding: utf-8

from pprint import pformat

from ..util import dprint, chunk, Line, Context


@Context.register
class Text:
	priority = -25
	PREFIX = '__w('
	SUFFIX = ')'
	
	def match(self, context, line):
		return line.kind == 'text'
	
	def __call__(self, context):
		input = context.input
		
		line = input.next()
		buffer = []
		
		if 'text' not in context.flag:
			yield Line(0, "")
			yield Line(0, "_buffer = []")
			yield Line(0, "__w = _buffer.append")
			yield Line(0, "")
			context.flag.add('text')
		
		while line.kind == 'text' or ( line.kind == 'comment' and line.stripped.startswith('#{') ):
			buffer.append(line.line.rstrip() + '\n')
			line = input.next()
		
		input.push(line)  # Put the last line back, as it won't be a text line.
		
		if __debug__: dprint("\x1b[34m", "?", "Text", len(buffer), "\x1b[0m")
		
		while buffer and not buffer[-1].strip():
			del buffer[-1]
			input.push(Line(0, ''))
		
		text = "".join(buffer)
		
		if text:
			context.flag.add('dirty')
		
		# We now have a contiguous block of templated text.  Now we need to split it up.
		
		for token, text in chunk(text):
			if token == 'text':
				yield Line(0, self.PREFIX + pformat(text, width=120 - 4 * context.scope) + self.SUFFIX)
			elif token == 'format':
				pass  # Need to think about that.
			else:
				yield Line(0, self.PREFIX + token + '(' + text + ')' + self.SUFFIX)
