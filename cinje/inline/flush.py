# encoding: utf-8

from ..util import Context, Line


def flush_template(context, declaration=None):
	"""Emit the code needed to flush the buffer.
		
	Will only emit the yield and clear if the buffer is known to be dirty.
	"""
	
	if declaration is None:
		declaration = Line(0, '')
	
	if 'text' not in context.flag or 'dirty' not in context.flag:
		return
	
	yield declaration.clone(line='yield "".join(_buffer)')
	yield declaration.clone(line='_buffer.clear()')
	
	context.flag.remove('dirty')



@Context.register
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
	"""
	
	priority = 25
	
	def match(self, context, line):
		"""Match exact "flush" command usage."""
		return line.kind == 'code' and line.stripped == "flush"
	
	def __call__(self, context):
		return flush_template(context, context.input.next())
