# encoding: utf-8

import pytest
import json
import os.path

from cinje.inline.use import Use
from cinje.util import flatten, fragment


def producer(*args, **kw):
	return [", ".join(str(i) for i in args) + "\n" + json.dumps(kw, sort_keys=True)]


@pytest.fixture
def tmpl():
	return fragment(': def consumer arg, *args, **kw\n\t: use arg *args, **kw')


class TestInlineUse(object):
	def test_simple(self, tmpl):
		assert flatten(tmpl(producer)) == '\n{}'
	
	def test_args(self, tmpl):
		assert flatten(tmpl(producer, 'foo', 'bar')) == "foo, bar\n{}"
	
	def test_kwargs(self, tmpl):
		assert flatten(tmpl(producer, name='foo', occupation='bar')) == '\n{"name": "foo", "occupation": "bar"}'
