# encoding: utf-8

from __future__ import print_function, unicode_literals

from cinje import transform

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter


try:
	import std  # Just import the template module as you would any other.
except:
	std = None


def dump(fragment, indent='\t'):
	print(indent + indent.join(fragment))


def main():
	global std
	
	print("Translated source code:\n")
	
	#with open('std.py', 'rb') as fh:
	#	content = fh.read()
	#	#print(content.decode('cinje'))
	#	
	#	lines = []
	#	
	#	for i in Context(content).stream:
	#		print('>', i)
	#		lines.append(str(i))
	
	#lines = "\n".join(lines)
	
	with open('std.py', 'rb') as fh:
		lines = transform(fh.read().decode('utf8'))
	
	print(highlight(lines, PythonLexer(), Terminal256Formatter()))
	
	if not std:
		import std
		return
	
	print("Here's a basic meta tag:\n")
	
	dump(std.meta("description", "This is a meta tag."))
	
	print("Here's something a bit more advanced:\n")
	
	for chunk in std.page_sample("<p>Content, eh?</p>"):
		print(">", repr(chunk))


if __name__ == '__main__':
	main()

