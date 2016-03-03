#encoding: utf-8

import sys


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
	
	def source(self, file):
		if file == '-':
			return self._source_string(sys.stdin.read())
		
		try:
			return self._source_reference(file)
		except ImportError:
			pass
		
		return self._source_path(file)
	
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
