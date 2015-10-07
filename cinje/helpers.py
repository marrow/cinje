# encoding: utf-8

try:  # pragma: no cover
	unicode = unicode
except:
	unicode = str

try:
	from markupsafe import Markup as bless, escape_silent as escape
except ImportError:
	bless = unicode
	try:
		from html import escape
	except:
		from cgi import escape

from .util import iterate, xmlargs, interruptable as _interrupt, Pipe as pipe


__all__ = ['unicode', 'bless', 'escape', 'iterate', 'xmlargs', '_interrupt', 'pipe']
