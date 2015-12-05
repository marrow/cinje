# encoding: utf-8

from __future__ import unicode_literals

import pytest
import os.path

from cinje.inline.require import Require


class TestInlineRequire(object):
	def test_import(self):
		assert 'from cinje.std.html import' in b': require cinje.std.html'.decode('cinje')
	
	def test_failure(self):
		with pytest.raises(ImportError):
			b': require cinje'.decode('cinje')
