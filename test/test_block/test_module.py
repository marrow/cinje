# encoding: utf-8

from __future__ import unicode_literals

import cinje


def test_module_preserves_prefix():
	assert '# xyzzy' in b'# xyzzy'.decode('cinje')


def test_module_strips_secret_prefix():
	assert 'xyzzy' not in b'## xyzzy'.decode('cinje')


def test_module_strips_encoding_prefix():
	assert 'coding' not in b'# encoding: cinje'.decode('cinje')
