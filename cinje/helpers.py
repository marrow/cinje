# encoding: utf-8

from __future__ import unicode_literals, print_function

import sys

from collections import Mapping
from json import dumps as _json

from marrow.dsl.compat import str
from .util import Pipe as pipe
from .util import interruptable as _interrupt
from .util import iterate as _iterate
from .util import stream as _stream
from .util import xmlargs as _xmlargs


try:
	from markupsafe import Markup as _bless, escape_silent as _escape

except ImportError:
	_bless = str
	
	try:
		from html import escape as __escape
	except:
		from cgi import escape as __escape
	
	def _escape(value):
		return __escape(str(value))


def _cmd(template, argv=None):
	"""Simplified command-line interface for template invocation.
	
	Positional arguments are supported, as are named keyword arguments in the forms `--key value` or `--key=value`.
	Some value interpolation is performed; numeric values will be integerized, and values may be JSON.
	"""
	
	argv = argv or sys.argv
	tmpl, arguments = argv[1], argv[2:]
	args = []
	kwargs = {}
	dumb = False
	pending = None
	
	def process(value):
		try:
			value = json.loads(value)
		except ValueError:
			pass
		
		return value
	
	for arg in arguments:
		if dumb:
			args.append(arg)
			continue
		
		if pending:
			kwargs[pending] = process(arg)
			pending = None
			continue
		
		if arg == '--':
			dumb = True
			continue
		
		if not arg.startswith('--'):
			args.append(arg)
			continue
		
		if '=' not in arg:
			pending = arg
			continue
		
		arg, sep, value = arg.partition('=')
		kwargs[arg] = process(value)
	
	if isinstance(template, Mapping):
		if tmpl not in template:
			print("Unknown template function: " + tmpl + " ", file=sys.stderr)
			print("Hint: execute symlinks to modules containing multiple templates.", file=sys.stderr, end="\n\n")
			print("", file=sys.stderr)
			print("Known template functions:", file=sys.stderr)
			for tmpl in sorted(template):
				print("* ", file=sys.stderr)
				
			sys.exit(1)
	
	return method_name, args, kwargs



__all__ = ['str', '_bless', '_escape', '_iterate', '_xmlargs', '_interrupt', 'pipe']
