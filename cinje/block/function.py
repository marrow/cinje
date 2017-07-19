# encoding: utf-8

from __future__ import unicode_literals

from marrow.dsl.block.function import FunctionTransformer
from ..inline.flush import flush_template
from ..util import ensure_buffer


log = __import__('logging').getLogger(__name__)


class CinjeFunctionTransformer(FunctionTransformer):
	"""Proces function declarations within templates.
	
	Used to track if the given function is a template function or not, transform the argument list if such optimization
	is warranted, and to add the requisite template processing glue suffix. Functions increase scope.
	
	Syntax:
	
		: def <name> <arguments>[ -> flag[, ...]]
		: end
	
	Inherits:
	
	* `name` - the name of the function
	* `buffer` - the named collection of buffers
	
	Tracks:
	
	* `helpers` - helpers utilized within this template function
	* `added` - context tags added via annotation
	* `removed` - context tags removed via annotation
	
	As a reminder, functions are divided into:
	
	* `decorator` - any leading `@decorator` invocations prior to the declaration
	* `declaration` - the function declaration itself as transformed by `process_declaration`
	* `docstring` - the initial documentation string, if present
	* `prefix` - any
	* `function`
	* `suffix`
	* `trailer`
	"""
	
	__slots__ = ('helpers', 'added', 'removed')
	
	def __init__(self, decoder):
		super(CinjeFunctionTransformer, self).__init__(decoder)
		
		self.helpers = set()  # Specific helpers utilized within the function.
		self.added = set()  # Flags added through annotation.
		self.removed = set()  # Flags removed through annotation.
	
	def process_declaration(self, context, declaration):
		line, = declaration  # Cinje declarations can only be one line... for now.
		
		text, _, annotation = line.line.partition(' ')[2].rpartition('->')
		
		if annotation and not text:  # Swap the values back.
			text = annotation
			annotation = ''
		
		name, _, text = text.partition(' ')  # Split the function name out.
		
		argspec = text.rstrip()
		name = self.name = name.strip()
		annotation = annotation.lstrip()
		annotation = {'!dirty', '!text', '!using'} | set(i.lower().strip() for i in annotation.split())
		
		# TODO: Re-introduce positional named local scoping optimization for non-Pypy runtimes.
		# TODO: Generalize flag processing like this into galfi.
		
		for flag in annotation:
			if not flag.strip('!'): continue  # Ignore standalone exclamation marks.
			
			if flag[0] == '!':
				flag = flag[1:]
				
				if flag in context:  # We do this rather than discard to track.
					context.remove(flag)
					self.removed.add(flag)
				
				continue
			
			if flag not in context:
				context.add(flag)
				self.added.add(flag)
		
		line = line.clone(line='def ' + name + '(' + argspec + '):')
		
		for line in super(CinjeFunctionTransformer, self).process_declaration(context, [line]):
			yield line
	
	def egress(self, context):
		"""Code to be executed when exiting the context of a function.
		
		Always call super() last in any subclasses.
		"""
		
		if 'dirty' in context:
			self.suffix.append(*flush_template(context, reconstruct=False))
		
		if 'text' in context:
			self.prefix.append(*ensure_buffer(context, False))
			context.module.templates.add(self.name)
		
		if 'using' in context:
			self.prefix.append('_using_stack = []')
		
		context.module.helpers.update(self.helpers)
		
		# Reset the manipulated flags to their original state.
		context.flag.discard(self.added)
		context.flag.update(self.removed)
