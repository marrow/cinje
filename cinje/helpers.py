# encoding: utf-8
# pragma: no cover

from json import dumps as _json

from .util import str, iterate, xmlargs, interruptable as _interrupt, Pipe as pipe

try:
	from markupsafe import Markup as bless, escape_silent as escape
except ImportError:
	bless = str
	try:
		from html import escape as __escape
	except:
		from cgi import escape as __escape
	
	def escape(value):
		return __escape(str(value))


__all__ = ['bless', 'escape', 'iterate', 'xmlargs', '_interrupt', 'pipe']
