# encoding: utf-8

from ..util import Line, ensure_buffer


def flush_template(context, declaration=None, reconstruct=True):
	"""Emit the code needed to flush the buffer.
		
	Will only emit the yield and clear if the buffer is known to be dirty.
	"""
	
	if declaration is None:
		declaration = Line(0, '')
	
	if {'text', 'dirty'}.issubset(context.flag):
		yield declaration.clone(line='yield "".join(_buffer)')
		
		context.flag.remove('text')  # This will force a new buffer to be constructed.
		context.flag.remove('dirty')
		
		if reconstruct:
			for i in ensure_buffer(context):
				yield i
	
	if declaration.stripped == 'yield':
		yield declaration


class Flush(object):
	"""Allow mid-stream flushing of the template buffer.
	
	This is generally used to flush sections of a page to the client to allow for content pre-loading of CSS,
	JavaScript, images, etc., as well as to provide a more responsive experience for a user during longer operations.
	
	Syntax:
	
		: flush
	
	Note: this will only emit the code needed to flush and clear the buffer if there is a buffer to flush, and the
	buffer is known to be "dirty" by the translator.  I.e. following ": use" or ": uses", or after some template
	text has been defined.  Unlike most other commands involving the buffer, this one will not create a buffer if
	missing.
	
	This also handles flushing prior to yielding, for wrapper templates.
	"""
	
	priority = 25
	
	def match(self, context, line):
		"""Match exact "flush" command usage."""
		return line.kind == 'code' and line.stripped in ("flush", "yield")
	
	def __call__(self, context):
		return flush_template(context, context.input.next())
