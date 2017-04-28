# encoding: utf-8

from __future__ import unicode_literals

from collections import defaultdict as ddict

from marrow.dsl.block.module import ModuleTransformer
from marrow.dsl.compat import py2, str
from marrow.dsl.core import Line


class CinjeModuleTransformer(ModuleTransformer):
	"""A cinje module.
	
	Where the base `ModuleTransformer` class handles line number mapping and `__futures__` imports for Python 2
	environments, this specialization adds template function name tracking, automatic importing of helpers, and
	in-development command-line interface `__main__` handler.
	
	Because cinje modules are so similar to standard Python modules, we don't actually have much work to do.
	
	Global processing flags:
	
	* `free` - If defined the resulting bytecode will have no runtime dependnecy on cinje itself.
	* `nomap` - Define to disable emission of line number mappings; this can speed up translation and reduce resulting
		bytecode size at the cost of increased debugging difficulty.
	* `raw` - Implies `free`; make no effort to sanitize output. This is **insecure**, but blazingly fast -- use with
		trusted or pre-sanitized input only!
	* `unbuffered` - utilize unbuffered output; fragments will be yielded as generated, buffer construction prefixes
		will not be generated
	
	Inherits:
	
	* `buffer` - The named collection of buffers.
	
	Tracks:
	
	* `templates` - The names of all module scoped template functions, as a set.
	* `helpers` - A set of declared used helpers, a shortcut for other transformers.
	* `_imports` - A mapping of packages to the set of objects acquired from within, from parent class.
	
	For reference, the buffers of a module are divided into:
	
	* `comment' - Shbang, encoding declaration, any additional leading comments and whitespace.
	* `docstring` - the docstring of the module, if present.
	* `imports` - the initial block of imports, including whitespace.
	* `prefix` - Any code to be inserted between imports and first non-import line.
	* `module` - The contents of the module proper.
	* `suffix` - Any code to be appended to the module, prior to the line mapping.
	"""
	
	__slots__ = ('templates', 'helpers')  # Additional data tracked by our specialization.
	
	# Line templates for easy re-use later.
	TEMPLATES = Line('__tmpl__ = ["{}"]')  # Used to record template functions at the module scope.
	MAIN = Line('if __name__ == "__main__":')  # Used with one of the following.
	SINGLE = Line('_cli({})', scope=1)  # There is only one template, so this is easy mode vs. the next.
	MULTI = Line('_cli({_tmpl: _tmpl_fn for _tmpl, _tmpl_fn in locals().items() if _tmpl in __tmpl__})', scope=1)
	
	def __init__(self, decoder):
		super(CinjeModuleTransformer, self).__init__(decoder)
		
		self.templates = set()  # The names of all module scoped template functions, as a set.
		self.helpers = {'str'} if py2 else set()  # Helpers to import 
	
	def egress(self, context):
		capable = not context.flag & {'free', 'raw'}
		
		if self.templates:
			suffix = self.suffix
			suffix.append('', self.TEMPLATES.format('", "'.join(self.templates)))
			
			if __debug__ and capable:
				self.helpers.add('_cli')
				suffix.append('', self.MAIN)
				
				if len(self.templates) == 1:
					tmpl, = self.templates
					suffix.append(self.SINGLE.format(tmpl))
				else:
					suffix.append(self.MULTI)
		
		if capable:
			self._imports['cinje.helper'].update(self.helpers)
		
		super(CinjeModuleTransformer, self).egress(context)
