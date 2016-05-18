# encoding: utf-8

from cinje import flatten
from typing import Iterable, Callable
from typeguard import check_argument_types
from asphalt.core import resolve_reference
from asphalt.templating.api import TemplateRenderer


class CinjeRenderer(TemplateRenderer):
	"""A convienence adapter for the Asphalt templating API.
	
	It is recommended to make direct use of cinje templates through import of template functions and direct execution
	instead of using this wrapper. Use of this wrapper will limit the functionality of the templates, preventing you
	from using the streaming and explicit flushing capabilities.
	"""
	
	__slots__ = ('packages', )
	
	def __init__(self, packages: Iterable[str] = ()):
		assert check_argument_types()
		self.packages = list(packages)
	
	def load_template(self, template: str) -> Callable:
		assert check_argument_types()
		
		if __debug__ and ':' not in template:  # A plain assertion says little about the type of error.
			raise ValueError("Template name must be a dot-colon reference to module:func.")
		
		for pkg in self.packages:
			try:
				return resolve_reference(pkg + '.' + template)
			except ImportError:
				pass
		else:
			return resolve_reference(template)
	
	def render(self, template: str, **kw) -> str:
		assert check_argument_types()
		func = self.load_template(template)
		result = func(**kw)  # Separated out on different lines to ease interactive debugging.
		return flatten(result)

