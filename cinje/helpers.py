# encoding: utf-8

from markupsafe import Markup as bless, escape_silent as escape

from .util import iterate, xmlargs, interruptable as _interrupt


__all__ = ['bless', 'escape', 'iterate', 'xmlargs', '_int']

