# encoding: utf-8

import ast  # Tighten your belts...

from pprint import pformat

from ..util import chunk, Line, ensure_buffer


class Text(object):
	"""Identify and process contiguous blocks of template text."""
	
	priority = -25
	PREFIX = '__w(('
	SUFFIX = '))'
	
	def match(self, context, line):
		return line.kind == 'text'
	
	def __call__(self, context):
		input = context.input
		
		# Make sure we have a buffer to write to.
		for i in ensure_buffer(context):
			yield i
		
		def gather():
			line = input.next()
			lead = True
			buffer = []
			
			# Gather contiguous (uninterrupted) lines of template text.
			while line.kind == 'text':
				value = line.line.rstrip().rstrip('\\') + ('' if line.continued else '\n')
				
				if lead and line.stripped:
					yield line.number, value
					lead = False
				
				elif not lead:
					if line.stripped:
						for buf in buffer:
							yield buf
						
						buffer = []
						yield line.number, value
					
					else:
						buffer.append((line.number, value))
				
				try:
					line = input.next()
				except StopIteration:
					line = None
					break
				
			if line:
				input.push(line)  # Put the last line back, as it won't be a text line.
		
		input.push(Line(0, ''))  # For code cleanlieness reasons, add some whitespace before a new block.
		
		text = "".join(i[1] for i in gather())
		
		# Track that the buffer will have content moving forward.  Used for conditional flushing.
		if text:
			context.flag.add('dirty')
		
		# We now have a contiguous block of templated text.  Split it up into expressions and wrap as appropriate.
		
		chunks = list(chunk(text))  # Ugh; this breaks streaming, but...
		single = len(chunks) == 1
		
		if single:
			PREFIX = '__ws('
		else:
			yield Line(0, '__w((')  # Start a call to _buffer.extend()
			PREFIX = ''
		
		for token, part in chunks:
			if token == 'text':
				part = pformat(
						part,
						indent = 0,
						width = 120 - 4 * (context.scope + (0 if single else 1)),
						# compact = True  Python 3 only.
					).replace("\n ", "\n" + "\t" * (context.scope + (0 if single else 1))).strip()
				
				if part[0] == '(' and part[-1] == ')':
					part = part[1:-1]
				
				yield Line(0, PREFIX + part + (')' if single else ','), (context.scope + (0 if single else 1)))
				continue
			
			elif token == 'format':
				# We need to split the expression defining the format string from the values to pass when formatting.
				# We want to allow any Python expression, so we'll need to piggyback on Python's own parser in order
				# to exploit the currently available syntax.  Apologies, this is probably the scariest thing in here.
				split = -1
				
				try:
					ast.parse(part)
				except SyntaxError as e:  # We expect this, and catch it.  It'll have exploded after the first expr.
					split = part.rfind(' ', 0, e.offset)
				
				token = '_bless(' + part[:split].rstrip() + ').format'
				part = part[split:].lstrip()
			
			yield Line(0, PREFIX + token + '(' + part + ')' + (')' if single else ','), (context.scope + (0 if single else 1)))
		
		if not single:
			yield Line(0, '))', (context.scope + 1))  # End the call to _buffer.extend()
