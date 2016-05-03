# encoding: utf-8


class Comment(object):
	"""Line comment handler.
	
	This handles not emitting double-hash comments and has a high priority to prevent other processing of
	commented-out lines.
	
	Syntax:
	
		# <comment>
		## <hidden comment>
	"""
	
	priority = -90
	
	def match(self, context, line):
		"""Match lines prefixed with a hash ("#") mark that don't look like text."""
		stripped = line.stripped
		return stripped.startswith('#') and not stripped.startswith('#{')
	
	def __call__(self, context):
		"""Emit comments into the final code that aren't marked as hidden/private."""
		
		line = context.input.next()
		
		if not line.stripped.startswith('##'):
			yield line
