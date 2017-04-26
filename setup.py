#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import os
import sys
import codecs


try:
	from setuptools.core import setup, find_packages
except ImportError:
	from setuptools import setup, find_packages


if sys.version_info < (2, 7):
	raise SystemExit("Python 2.7 or later is required.")
elif sys.version_info > (3, 0) and sys.version_info < (3, 3):
	raise SystemExit("CPython 3.3 or compatible Pypy or later is required.")

version = description = url = author = author_email = ""  # Silence linter warnings.
exec(open(os.path.join("cinje", "release.py")).read())  # Actually populate those values.

here = os.path.abspath(os.path.dirname(__file__))

tests_require = [
		'pytest',  # test collector and extensible runner
		'pytest-cov',  # coverage reporting
		'pytest-flakes',  # syntax validation
		'pytest-capturelog',  # log capture
	]

if 'ACCELERATED' not in os.environ or os.environ.get('ACCELERATED', '1') != '0':
	tests_require.append('markupsafe')  # Data safety helper.


setup(
	name = "cinje",
	version = version,
	description = description,
	long_description = codecs.open(os.path.join(here, 'README.rst'), 'r', 'utf8').read(),
	url = url,
	download_url = 'https://github.com/marrow/cinje/releases',
	author = author.name,
	author_email = author.email,
	license = 'MIT',
	keywords = ['template', 'source translation', 'dsl', 'streaming', 'chunked'],
	classifiers = [
			"Development Status :: 5 - Production/Stable",
			"Environment :: Console",
			"Environment :: Web Environment",
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python :: 2",
			"Programming Language :: Python :: 2.7",
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.2",
			"Programming Language :: Python :: 3.3",
			"Programming Language :: Python :: 3.4",
			"Programming Language :: Python :: 3.5",
			"Programming Language :: Python :: 3.6",
			"Programming Language :: Python :: Implementation :: CPython",
			"Programming Language :: Python :: Implementation :: PyPy",
			"Programming Language :: Python",
			"Topic :: Internet :: WWW/HTTP :: Dynamic Content",
			"Topic :: Internet :: WWW/HTTP :: WSGI",
			"Topic :: Software Development :: Libraries :: Python Modules",
			"Topic :: Software Development :: Libraries",
			"Topic :: Utilities",
		],
	
	packages = find_packages(exclude=['bench', 'docs', 'example', 'test', 'htmlcov']),
	include_package_data = True,
	package_data = {'': ['README.rst', 'LICENSE.txt']},
	namespace_packages = ['marrow'],
	zip_safe = True,
	
	entry_points = {
			'marrow.dsl': [
					'cinje = cinje.decoder:CinjeDecoder',
				],
			
			'marrow.dsl.cinje': [  # Core namespace.
					# Cinje Line Classifiers
					'scope = cinje.classify:CinjeScopeClassifier',
					'line = cinje.classify:CinjeLineClassifier',
					
					# Block Transformers
					'module = cinje.block.module:CinjeModuleTransformer',
					#'function = cinje.block.function:CinjeFunctionTransformer',
					#'generic = cinje.block.generic:Generic',
					#'using = cinje.block.using:Using',
					
					# Inline Transformers
					#'blank = cinje.inline.blank:Blank',
					#'code = cinje.inline.code:Code',
					#'comment = cinje.inline.comment:Comment',  # see TODO from cinje.classify
					#'flush = cinje.inline.flush:Flush',
					#'require = cinje.inline.require:Require',
					#'use = cinje.inline.use:Use',
					#'pragma = cinje.inline.pragma:Pragma',
				],
			
			'marrow.dsl.cinje.html': [  # HTML-specific string safety helpers and adaptions.
					# 'text = cinje.inline.text:CinjeHTMLTransformer',
				],
			
			'marrow.dsl.cinje.xml': [  # XML-specific string safety helpers and adaptions.
					# 'text = cinje.inline.text:CinjeXMLTransformer',
				],
		},
	
	setup_requires = [
			'pytest-runner',
		] if {'pytest', 'test', 'ptr'}.intersection(sys.argv) else [],
	install_requires = [],
	tests_require = tests_require,
	extras_require = {
			'development': tests_require + ['pre-commit'],  # Development requirements are the testing requirements.
			'safe': ['markupsafe'],  # String safety.
		},
)
