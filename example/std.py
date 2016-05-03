# encoding: utf-8

from __future__ import print_function, unicode_literals

import cinje
import cinje.std.html

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter


def main():
	print("Translated source code:\n")
	
	lines = open(cinje.std.html.__file__.replace('.pyc', '.py'), 'rb').read().decode('cinje')
	
	print(highlight(lines, PythonLexer(), Terminal256Formatter()))


if __name__ == '__main__':
	main()
