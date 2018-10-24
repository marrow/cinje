# encoding: utf-8

from __future__ import unicode_literals

import pytest
from cinje import fragment
from cinje.util import flatten



@pytest.fixture
def tmpl():
	__import__('pudb').set_trace()
	return fragment("Epic Template™".encode('utf-8'), name="tmpl")


class TestIssueTwentyFive(object):
	def test_trademark(self, tmpl):
		assert flatten(tmpl()) == 'Epic Template™\n'
