# encoding: utf-8

"""Because this is all related functionality, this tests all of the individual code sites involved in unbuffered text
processing."""

from __future__ import unicode_literals


from cinje.util import str, Context


class Emit(object):
	"""Spit out the current flags when asked."""
	
	priority = -100
	
	def match(self, context, line):
		return line.kind == 'code' and line.stripped.startswith('emit')
	
	def __call__(self, context):
		line = context.input.next()
		yield line.clone(line='flags: ' + ', '.join(sorted(context.flag)))


def process(sample):
	"""Process a sample template through a patched engine."""
	c = Context(sample)
	c.handlers.append(Emit)  # Add our little "extension" from above.
	return list(i for i in c.stream if i.line.startswith('flags: '))


def test_function_flag_addition():
	result = process(""": emit\n\n: def foo -> example\n\n: emit\n\n: end\n\n: emit""")
	pre, mid, post = result
	
	assert str(pre).strip() == 'flags: buffer, init'
	assert str(mid).strip() == 'flags: buffer, example, init, text'
	assert str(post).strip() == 'flags: buffer, init'


def test_function_flag_removal():
	result = process(""": emit\n\n: def foo -> !buffer\n\n: emit\n\n: end\n\n: emit""")
	pre, mid, post = result
	
	assert str(pre).strip() == 'flags: buffer, init'
	assert str(mid).strip() == 'flags: init'
	assert str(post).strip() == 'flags: buffer, init'


def test_buffer_aware_use():
	result = b": def foo -> !buffer\n\n: use bar args".decode('cinje')
	
	assert 'bar(args)' in result
	assert 'yield from' in result or 'for _chunk in' in result


def test_pragma_additions():
	result = process(""": emit\n\n: pragma foo\n\n: emit""")
	
	first, second = result
	assert str(first).strip() == 'flags: buffer, init'
	assert str(second).strip() == 'flags: buffer, foo, init'


def test_pragma_removal():
	result = process(""": emit\n\n: pragma !buffer\n\n: emit""")
	
	first, second = result
	assert str(first).strip() == 'flags: buffer, init'
	assert str(second).strip() == 'flags: init'

