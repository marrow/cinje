# encoding: utf-8


class Pragma(object):
	"""Allow the addition and removal of translation flags during the translation process.
	
	Usage is straightforward; to add "flag" to the current set of flags:
	
		: pragma flag
	
	To subsequently remove a flag:
	
		: pragma !flag
	
	Multiple flags may be whitespace separated and can mix addition and removal:
	
		: pragma flag !other_flag
	
	No flag may contain whitespace.
	
	Built-in flags include:
	
		`init`: The module scope has been prepared. Unsetting this is unwise.
		
		`text`: Text fragments have been utilized within the current function scope.
		
		`dirty`: It is known to the engine that the current buffer contains content which will need to be flushed.
		
		`buffer`: Enabled by default, its presence tells cinje to use a buffer with explicit flushing. When removed
				buffering is disabled and every fragment is flushed as it is encounered and `: use` / `: using`
				behaviour is altered to `yield from` instead of adding the child template to the buffer.
				
				It is potentially very useful to disable this in the context of `: use` and `: using` to make child
				template `: flush` statements effective.
		
		`using`: Indicates the `_using_stack` variable is available at this point in the translated code, i.e. to
				track nested `: using` statements.
	
	In Python 3 runtimes with function annotation support, you can declare flags as the return type annotation:
	
		: def my_function argument, other_argument -> 'flag !other_flag'
	
	Flags declared this way will have their effect reversed automatically at the close of the function scope.
	"""
	
	priority = 25
	
	def match(self, context, line):
		"""Match "pragma" command usage."""
		return line.kind == 'code' and line.stripped.startswith('pragma ')
	
	def __call__(self, context):
		# Pull out the flags from the pragma line, ignoring the initial "pragma" that will be present.
		flags = [i.lower().strip() for i in context.input.next().stripped.split()][1:]
		
		# Iterate through the flags and set or unset them as appropriate:
		for flag in flags:
			if not flag.strip('!'): continue  # Handle the edge case of a standalone "!".
			
			if flag[0] == '!':
				flag = flag[1:]
				
				if flag in context.flag:
					context.flag.remove(flag)
				
				continue
			
			if flag not in context.flag:
				context.flag.add(flag)
		
		if False:  # We need to be a generator, but we don't generate anything.
			yield

