#encoding: utf-8

import sys

try:
	import pygments
	import pygments.lexers
	import pygments.formatters
except ImportError:
	pygments = None


from cinje import flatten


class CommandLineInterface(object):
	def __init__(self, arguments):
		remainder = list(arguments)
		kwargs = list((i, remainder.pop(i), v.partition('=')) for i, v in reversed(list(enumerate(arguments))) if v.startswith('--'))
		self.kwargs = {k[2:]: v for i, (k, _, v) in kwargs}
		self.flags = set(remainder.pop(i)[1:] for i, v in reversed(list(enumerate(remainder))) if v.startswith('-'))
		self.args = remainder
	
	def go(self, action, *args, **data):
		action = getattr(self, action)
		result = action(*args, **data)
		if isinstance(result, int):
			sys.exit(result)
		if result:
			print(result)
	
	def render(self, reference, *args, **kw):
		output = kw.pop('out', None)
		encoding = kw.pop('encoding', 'utf8')
		
		module, _, function = reference.partition(':')
		module = __import__(module, fromlist=(function, ))
		template = getattr(module, function)(*args, **kw)
		
		if output and output != '-':
			with open(output, 'wb') as fh:
				flatten(template, fh, encoding=encoding)
			
			return '' if 'q' in self.flags else ("Template result written to: " + output)
		
		if pygments and (sys.stdout.isatty() or 'c' in self.flags) and 'C' not in self.flags:
			language = pygments.lexers.get_lexer_by_name('html')
			formatter = pygments.formatters.get_formatter_by_name('256')
			return pygments.highlight(flatten(template), language, formatter)
		
		flatten(template, sys.stdout)
	
	def source(self, file):
		result = None
		
		if file == '-':
			result = self._source_string(sys.stdin.read())
		else:
			try:
				result = self._source_reference(file)
			except ImportError:
				result = self._source_path(file)
		
		if pygments and (sys.stdout.isatty() or 'c' in self.flags) and 'C' not in self.flags:
			language = pygments.lexers.get_lexer_by_name('python')
			language.add_filter('highlight', names=[
					'__w', '__ws', '_bless', '_escape', '_args',
				])
			formatter = pygments.formatters.get_formatter_by_name('256')
			return pygments.highlight(result, language, formatter)
		
		return result
	
	def _source_reference(self, reference):
		parts = reference.split('.')[1:]
		root = __import__(reference)
		for part in parts:
			root = getattr(root, part)
		return self._source_path(root.__file__)
	
	def _source_string(self, string):
		return string.encode('utf8').decode('cinje')
	
	def _source_path(self, path):
		with open(path, 'rb') as fh:
			return fh.read().decode('cinje')


if __name__ == '__main__':
	# Standard armour.
	interface = CommandLineInterface(sys.argv[1:])
	interface.go(*interface.args, **interface.kwargs)
