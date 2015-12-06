# encoding: utf-8

from __future__ import print_function, unicode_literals

from cinje import transform

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter


def main():
	with open('../cinje/std/form/select.py', 'rb') as fh:
		lines = transform(fh.read().decode('utf8'))
	
	print(highlight(lines, PythonLexer(), Terminal256Formatter()))


if __name__ == '__main__':
	main()

