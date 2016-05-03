# encoding: utf-8


class Generic(object):
	"""Block-level passthrough.  Blocks must be terminated by ": end" markers.
	
	Support is included for chains of blocks of the expected types, without requiring ": end" markers between them.
	
	This block-level transformer handles: "if", "elif", and "else" conditional scopes; "while" and "for" loops,
	including the optional "else" clause to "for"; "with" context managers; and the exception management machinery of
	"try", "except", "finally", and "else".  (Any given intermediary component is optional, of course.)
	
	Syntax::
	
		: if ...
		: elif ...
		: else
		: end
		
		: while ...
		: end
		
		: for ...
		: else
		: end
		
		: with ...
		: end
		
		: try
		: except ...
		: finally
		: else
		: end
	
	Single-line conditionals and loops are not allowed, and the declaration should not include a trailing colon.
	"""
	
	priority = 50
	
	_keywords = (
			'if',
			'while',
			'for',
			'with',
			'try',
		)
	_continuation = (
			'elif',
			'else',
			'except',
			'finally',
		)
	_both = _keywords + _continuation
	
	def match(self, context, line):
		"""Match code lines prefixed with a variety of keywords."""
		
		return line.kind == 'code' and line.partitioned[0] in self._both
	
	def __call__(self, context):
		"""Process conditional declarations."""
		
		input = context.input
		
		declaration = input.next()
		stripped = declaration.stripped
		prefix, _ = declaration.partitioned
		
		if prefix in self._continuation:  # We're handling an alternate section...
			yield declaration.clone(line=stripped + ':', scope=context.scope - 1)
			return  # We're done here.
		
		yield declaration.clone(line=stripped + ':')
		
		context.scope += 1
		
		for i in context.stream:
			yield i
		
		context.scope -= 1
