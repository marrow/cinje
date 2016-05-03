# encoding: utf-8

from importlib import import_module


class Require(object):
	"""Include reusable components from other modules.
	
	Does what is nessicary to discover template functions and construct complete imports template-side.
	
	Syntax:
	
		: require package.subpackage.module
	
	All template functions in the target namespace will be imported.
	"""
	
	priority = 25
	
	def match(self, context, line):
		"""Match code lines prefixed with a "require" keyword."""
		return line.kind == 'code' and line.partitioned[0] == "require"
	
	def __call__(self, context):
		"""Identify template functions in the target namespace, and construct the import line for them."""
		
		input = context.input
		
		declaration = input.next()
		namespace = declaration.partitioned[1]  # Ignore the "require" part, we care about the namepsace.
		
		module = import_module(namespace)
		
		if not hasattr(module, '__tmpl__'):
			raise ImportError("Attempted to require " + namespace + ", which contains no template functions.")
		
		yield declaration.clone(line="from " + namespace + " import " + ", ".join(module.__tmpl__))
