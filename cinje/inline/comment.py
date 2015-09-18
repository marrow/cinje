# encoding: utf-8

from ..util import dprint, Context


@Context.register
class Comment:
	"""Line comment handler.
	
	This handles not emitting double-hash comments and has a high priority to prevent other processing of commented-out lines.
	"""
	
	priority = -90
	
	def match(self, context, line):
		return line.stripped and line.stripped[0] == '#'
	
	def __call__(self, context):
		line = context.input.next()
		
		if __debug__: dprint("\x1b[34m", "?", "Comment", line, "\x1b[0m")
		
		if not line.stripped.startswith('##'):
			yield line
