# encoding: utf-8

import pytest
import json
import os.path

from cinje.inline.use import Use
from cinje.util import s


def producer(*args, **kw):
	return [", ".join(str(i) for i in args) + "\n" + json.dumps(kw, sort_keys=True)]


@pytest.fixture
def tmpl():
	env = dict()
	src = b': def consumer arg, *args, **kw\n\t: use arg *args, **kw'.decode('cinje')
	exec(src, env)
	return env['consumer']


class TestInlineUse(object):
	def test_simple(self, tmpl):
		assert s(tmpl(producer)) == '\n{}'
	
	def test_args(self, tmpl):
		assert s(tmpl(producer, 'foo', 'bar')) == "foo, bar\n{}"
	
	def test_kwargs(self, tmpl):
		assert s(tmpl(producer, name='foo', occupation='bar')) == '\n{"name": "foo", "occupation": "bar"}'
