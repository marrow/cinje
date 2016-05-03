# encoding: utf-8

import re

from ..util import py, pypy, ensure_buffer
from ..inline.flush import flush_template



class Function(object):
	"""Proces function declarations within templates.
	
	Syntax:
	
		: def <name> <arguments>
		: end
	
	"""
	
	priority = -50
	
	# Patterns to search for bare *, *args, or **kwargs declarations.
	STARARGS = re.compile(r'(^|,\s*)\*([^*\s,]+|\s*,|$)')
	STARSTARARGS = re.compile(r'(^|,\s*)\*\*\S+')
	
	# Automatically add these as keyword-only scope assignments.
	OPTIMIZE = ['_escape', '_bless', '_args']
	
	def match(self, context, line):
		"""Match code lines using the "def" keyword."""
		return line.kind == 'code' and line.partitioned[0] == 'def'
	
	def _optimize(self, context, argspec):
		"""Inject speedup shortcut bindings into the argument specification for a function.
		
		This assigns these labels to the local scope, avoiding a cascade through to globals(), saving time.
		
		This also has some unfortunate side-effects for using these sentinels in argument default values!
		"""
		
		argspec = argspec.strip()
		optimization = ", ".join(i + "=" + i for i in self.OPTIMIZE)
		split = None
		prefix = ''
		suffix = ''
		
		if argspec:
			matches = list(self.STARARGS.finditer(argspec))
			
			if matches:
				split = matches[-1].span()[1]  # Inject after, a la "*args>_<", as we're positional-only arguments.
				if split != len(argspec):
					prefix = ', ' if argspec[split] == ',' else ''
					suffix = '' if argspec[split] == ',' else ', ' 
			
			else:  # Ok, we can do this a different way…
				matches = list(self.STARSTARARGS.finditer(argspec))
				prefix = ', *, '
				suffix = ', '
				if matches:
					split = matches[-1].span()[0]  # Inject before, a la ">_<**kwargs".  We're positional-only arguments.
					if split == 0:
						prefix = '*, '
					else:
						suffix = ''
				else:
					split = len(argspec)
					suffix = ''
		
		else:
			prefix = '*, '
		
		if split is None:
			return prefix + optimization + suffix
		
		return argspec[:split] + prefix + optimization + suffix + argspec[split:]
	
	def __call__(self, context):
		input = context.input
		
		declaration = input.next()
		line = declaration.partitioned[1]  # We don't care about the "def".
		line, _, annotation = line.rpartition('->')
		
		if annotation and not line:  # Swap the values back.
			line = annotation
			annotation = ''
		
		name, _, line = line.partition(' ')  # Split the function name.
		
		argspec = line.rstrip()
		name = name.strip()
		annotation = annotation.lstrip()
		added_flags = []
		removed_flags = []
		
		if annotation:
			for flag in (i.lower().strip() for i in annotation.split()):
				if not flag.strip('!'): continue  # Handle standalone exclamation marks.
				
				if flag[0] == '!':
					flag = flag[1:]
					
					if flag in context.flag:
						context.flag.remove(flag)
						removed_flags.append(flag)
					
					continue
				
				if flag not in context.flag:
					context.flag.add(flag)
					added_flags.append(flag)
		
		if py == 3 and not pypy:
			argspec = self._optimize(context, argspec)
		
		# Reconstruct the line.
		
		line = 'def ' + name + '(' + argspec + '):'
		
		# yield declaration.clone(line='@cinje.Function.prepare')  # This lets us do some work before and after runtime.
		yield declaration.clone(line=line)
		
		context.scope += 1
		
		for i in ensure_buffer(context, False):
			yield i
		
		for i in context.stream:
			yield i
		
		if 'using' in context.flag:  # Clean up that we were using things.
			context.flag.remove('using')
		
		if 'text' in context.flag:
			context.templates.append(name)
		
		for i in flush_template(context, reconstruct=False):  # Handle the final buffer yield if any content was generated.
			yield i
		
		if 'text' in context.flag:
			context.flag.remove('text')
		
		for flag in added_flags:
			if flag in context.flag:
				context.flag.remove(flag)
		
		for flag in removed_flags:
			if flag not in context.flag:
				context.flag.add(flag)
		
		context.scope -= 1

