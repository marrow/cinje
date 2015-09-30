# encoding: utf-8

from ..util import Context
from .flush import flush_template


@Context.register
class Inline(object):
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
		"""Match bare "yield" usage."""
		return line.kind == 'code' and line.stripped == "yield"
	
	def __call__(self, context):
		input = context.input
		
		declaration = context.input.next()
		
		for i in flush_template(context, declaration):
			yield i
		
		yield declaration
