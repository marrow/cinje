# encoding: utf-8

import re

from ..util import dprint, Line, Context


@Context.register
class Function:
	priority = -50
	
	STARARGS = re.compile(r'(^|,\s*)\*([^*\s,]+|\s*,|$)')
	STARSTARARGS = re.compile(r'(^|,\s*)\*\*\S+')
	STAR = re.compile(r'\*,')
	
	OPTIMIZE = ['_escape', '_bless', '_args']
	
	def match(self, context, line):
		return line.kind == 'code' and line.stripped.startswith('def ')
	
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
					prefix = ' ' if argspec[split] in (',', ' ') else ', '
					suffix = ','
			
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
		
		if __debug__: dprint("\x1b[33;1m", "+", "Function", "\x1b[0m")
		
		declaration = input.next()
		line = declaration.stripped
		
		# To-do: this is atrocious.  Use a real parser.
		_, _, line = line.partition(' ')  # Clear out the "def".
		name, _, line = line.partition(' ')  # Split the function name.
		
		# We want to preserve function annottations.
		# However, without a closing ), how do you determine this?
		# -> might be within a string…, making this code break the users!
		
		argspec = line
		annotation = None
		
		if '->' in line:
			if '->' in line and line.rfind('->') > line.rfind(','):  # TODO: This just makes the edge case slightly edgier.
				argspec, _, annotation = line.rpartition('->')
		
		name = name.strip()
		argspec = self._optimize(context, argspec)
		
		if annotation:
			annotation = annotation.strip()
		
		# Reconstruct the line.
		
		line = 'def ' + name + '(' + argspec + '):' + ((' -> ' + annotation) if annotation else '')
		
		yield declaration.clone(line='@cinje.Function.prepare')  # This lets us do some work before and after runtime.
		yield declaration.clone(line=line)
		
		context.scope += 1
		yield from context.stream  # Descend into the function's scope.
		
		if 'using' in context.flag:  # Clean up that we were using things.
			context.flag.remove('using')
		
		if 'text' in context.flag:  # Handle the final buffer yield if any content was generated.
			context.flag.remove('text')
		
		if 'dirty' in context.flag:  # Handle the final buffer yield if any content was generated.
			context.flag.remove('dirty')
			yield Line(0, '')
			yield Line(0, 'yield "".join(_buffer)')
		
		context.scope -= 1
		if __debug__: dprint("\x1b[33m", "-", "Function", "\x1b[0m")
	
	@classmethod
	def prepare(cls, fn):
		# Decorator hook.
		return fn
