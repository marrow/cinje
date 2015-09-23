# encoding: utf-8

try:
	from markupsafe import Markup as bless, escape_silent as escape
except ImportError:
	bless = str
	from html import escape

from .util import iterate, xmlargs, interruptable as _interrupt


__all__ = ['bless', 'escape', 'iterate', 'xmlargs', '_int']

