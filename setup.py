#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import codecs

try:
	from setuptools.core import setup, find_packages
except ImportError:
	from setuptools import setup, find_packages

from setuptools.command.test import test as TestCommand


if sys.version_info < (2, 6):
	raise SystemExit("Python 2.6 or later is required.")
elif sys.version_info > (3, 0) and sys.version_info < (3, 2):
	raise SystemExit("Python 3.2 or later is required.")

exec(open(os.path.join("cinje", "release.py")).read())


class PyTest(TestCommand):
	def finalize_options(self):
		TestCommand.finalize_options(self)
		
		self.test_args = []
		self.test_suite = True
	
	def run_tests(self):
		import pytest
		sys.exit(pytest.main(self.test_args))


here = os.path.abspath(os.path.dirname(__file__))

tests_require = ['pytest', 'pytest-cov', 'pytest-spec', 'pytest-flakes']

if 'ACCELERATED' not in os.environ or os.environ.get('ACCELERATED', '1') != '0':
	tests_require.append('markupsafe')


# # Entry Point

setup(
	name = "cinje",
	version = version,
	
	description = description,
	long_description = codecs.open(os.path.join(here, 'README.rst'), 'r', 'utf8').read(),
	url = url,
	
	author = author.name,
	author_email = author.email,
	
	license = 'MIT',
	keywords = ['template', 'source translation', 'dsl', 'streaming', 'chunked'],
	classifiers = [
			"Development Status :: 5 - Production/Stable",
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python",
			"Programming Language :: Python :: 2",
			"Programming Language :: Python :: 2.7",
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.2",
			"Programming Language :: Python :: 3.3",
			"Programming Language :: Python :: 3.4",
			"Programming Language :: Python :: 3.5",
			"Programming Language :: Python :: Implementation :: CPython",
			"Programming Language :: Python :: Implementation :: PyPy",
			"Topic :: Software Development :: Libraries :: Python Modules",
			"Topic :: Utilities"
		],
	
	packages = find_packages(exclude=['test', 'example', 'benchmark']),
	include_package_data = True,
	package_data = {'': ['README.rst', 'LICENSE.txt']},
	
	# ## Dependency Declaration
	
	install_requires = [],
	
	extras_require = dict(
			development = tests_require,
		),
	
	tests_require = tests_require,
	
	# ## Plugin Registration
	
	entry_points = {
				'cinje.translator': [
						# ### Block Translators
						'function = cinje.block.function:Function',
						'generic = cinje.block.generic:Generic',
						'module = cinje.block.module:Module',
						'using = cinje.block.using:Using',
						
						# ### Inline Translators
						'blank = cinje.inline.blank:Blank',
						'code = cinje.inline.code:Code',
						'comment = cinje.inline.comment:Comment',
						'flush = cinje.inline.flush:Flush',
						'require = cinje.inline.require:Require',
						'text = cinje.inline.text:Text',
						'use = cinje.inline.use:Use',
						'pragma = cinje.inline.pragma:Pragma',
					]
			},
	
	zip_safe = False,
	cmdclass = dict(
			test = PyTest,
		)
)
