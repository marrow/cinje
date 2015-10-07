# encoding: utf-8

from pprint import pformat

from ..util import chunk, Line, Context, ensure_buffer


@Context.register
class Text(object):
	"""Identify and process contiguous blocks of template text."""
	
	priority = -25
	PREFIX = '__w(('
	SUFFIX = '))'
	
	def match(self, context, line):
		return line.kind == 'text'
	
	def __call__(self, context):
		input = context.input
		
		line = input.next()
		buffer = []
		
		# Make sure we have a buffer to write to.
		for i in ensure_buffer(context):
			yield i
		
		# Gather contiguous (uninterrupted) lines of template text.
		while line.kind == 'text' or ( line.kind == 'comment' and line.stripped.startswith('#{') ):
			buffer.append(line.line.rstrip().rstrip('\\') + ('' if line.continued else '\n'))
			try:
				line = input.next()
			except StopIteration:
				line = None
				break
		
		if line:
			input.push(line)  # Put the last line back, as it won't be a text line.
		
		# Eliminate trailing blank lines.
		while buffer and not buffer[-1].strip():
			del buffer[-1]
			input.push(Line(0, ''))
		
		text = "".join(buffer)
		
		# Track that the buffer will have content moving forward.  Used for conditional flushing.
		if text:
			context.flag.add('dirty')
		
		# We now have a contiguous block of templated text.  Split it up into expressions and wrap as appropriate.
		
		yield Line(0, self.PREFIX)  # Start a call to _buffer.extend()
		
		for token, part in chunk(text):
			if token == 'text':
				part = pformat(
						part,
						indent = 0,
						width = 120 - 4 * (context.scope + 1),
						# compact = True  Python 3 only.
					).replace("\n ", "\n" + "\t" * (context.scope + 1)).strip()
				
				if part[0] == '(' and part[-1] == ')':
					part = part[1:-1]
				
				yield Line(0, part + ',', (context.scope + 1))
			
			elif token == 'format':
				pass  # TODO: Need to think about that.
			
			elif token != '':
				yield Line(0, token + '(' + part + '),', (context.scope + 1))
			
			else:
				yield Line(0, '_escape(' + part + '),', (context.scope + 1))
		
		yield Line(0, self.SUFFIX, (context.scope + 1))  # End the call to _buffer.extend()
