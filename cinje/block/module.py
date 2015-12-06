# encoding: utf-8

from pprint import pformat
from collections import deque

from ..util import py, Line


class Module(object):
	"""Module handler.
	
	This is the initial scope, and the highest priority to ensure its processing of the preamble happens first.
	"""
	
	priority = -100
	
	def match(self, context, line):
		return 'init' not in context.flag
	
	def __call__(self, context):
		input = context.input
		
		context.flag.add('init')
		
		imported = False
		
		for line in input:
			if not line.stripped or line.stripped[0] == '#':
				if not line.stripped.startswith('##') and 'coding:' not in line.stripped:
					yield line
				continue
			
			input.push(line)  # We're out of the preamble, so put that line back and stop.
			break
		
		# After any existing preamble, but before other imports, we inject our own.
		
		if py == 2:
			yield Line(0, 'from __future__ import unicode_literals')
			yield Line(0, '')
		
		yield Line(0, 'import cinje')
		yield Line(0, 'from cinje.helpers import escape as _escape, bless as _bless, iterate, xmlargs as _args, _interrupt, _json')
		yield Line(0, '')
		yield Line(0, '')
		yield Line(0, '__tmpl__ = []  # Exported template functions.')
		yield Line(0, '')
		
		for i in context.stream:
			yield i
		
		if context.templates:
			yield Line(0, '')
			yield Line(0, '__tmpl__.extend(["' + '", "'.join(context.templates) + '"])')
			context.templates = []
		
		# Snapshot the line number mapping.
		# TODO: Run-length encode the line number deltas, 'cause damn, this is a lot of data.
		mapping = deque(context.mapping)
		mapping.reverse()
		
		mapping = deque(pformat(list(mapping), indent=0, width=105).split('\n'))
		
		yield Line(0, '')
		yield Line(0, '__mapping__ = ' + mapping.popleft())
		for line in mapping:
			yield Line(0, line)
		
		context.flag.remove('init')
