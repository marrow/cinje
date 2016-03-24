# encoding: utf-8

import ast  # Tighten your belts...

from pprint import pformat

from ..util import pypy, iterate, chunk, Line, ensure_buffer


def gather(input):
	"""Collect contiguous lines of text, preserving line numbers."""
	
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


class Text(object):
	"""Identify and process contiguous blocks of template text."""
	
	priority = -25
	PREFIX = '_buffer.extend((' if pypy else '__w(('
	PREFIX_SINGLE = '_buffer.append(' if pypy else '__ws('
	SUFFIX = '))'
	SUFFIX_SINGLE = ')'
	
	def match(self, context, line):
		return line.kind == 'text'
	
	def process_text(self, chunk_, scope, lineno, prefix, suffix, last, first):
		chunk_ = pformat(
				chunk_,
				indent = 0,
				width = 120 - 4 * scope,
			).replace("\n ", "\n").strip().lstrip('(').rstrip(')')
		
		for line in iterate(chunk_.split('\n')):
			value = line.value
			
			if line.first and prefix:
				value = prefix + value
			
			if suffix:
				value += suffix
			
			yield Line(lineno, value, scope)
		
		if last and not first:
			yield Line(lineno, self.SUFFIX, scope - 1)  # End the call to _buffer.extend()
	
	def process_format(self, chunk_):
		# We need to split the expression defining the format string from the values to pass when formatting.
		# We want to allow any Python expression, so we'll need to piggyback on Python's own parser in order
		# to exploit the currently available syntax.  Apologies, this is probably the scariest thing in here.
		split = -1
		
		try:
			ast.parse(chunk_)
		except SyntaxError as e:  # We expect this, and catch it.  It'll have exploded after the first expr.
			split = chunk_.rfind(' ', 0, e.offset)
		
		token = '_bless(' + chunk_[:split].rstrip() + ').format'
		chunk_ = chunk_[split:].lstrip()
		
		return token, chunk_
	
	def __call__(self, context):
		dirty = False  # Used for conditional flushing.
		prefix = ''  # Prepend to the source line emitted.
		suffix = ''  # Append to the source line emitted.
		
		# Make sure we have a buffer to write to.
		for i in ensure_buffer(context):
			yield i
		
		lines = gather(context.input)
		
		def inner_chain():
			for lineno, line in lines:
				for inner_chunk in chunk(line):
					yield lineno, inner_chunk
		
		chunks = inner_chain()
		
		for first, last, index, total, (lineno, (token, chunk_)) in iterate(chunks):
			prefix = ''
			suffix = ''
			scope = context.scope + 1
			dirty = True
			
			if first and last:  # Optimize the single invocation case.
				prefix = self.PREFIX_SINGLE
				suffix = self.SUFFIX_SINGLE
				scope = context.scope
			
			elif first:
				yield Line(lineno, self.PREFIX)
			
			if not last:
				suffix += ','
			
			if token == 'text':
				for line in self.process_text(chunk_, scope, lineno, prefix, suffix, last, first):
					yield line
				
				continue
			
			if token == 'format':
				token, chunk_ = self.process_format(chunk_)
			
			yield Line(lineno, prefix + token + '(' + chunk_ + ')' + suffix, scope)
			
			if last and not first:
				yield Line(lineno, self.SUFFIX, scope - 1)  # End the call to _buffer.extend()
		
		# Track that the buffer will have content moving forward.
		if dirty and 'dirty' not in context.flag:
			context.flag.add('dirty')
