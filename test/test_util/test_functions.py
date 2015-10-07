# encoding: utf-8

from cinje.util import interruptable, iterate, xmlargs, chunk

# Note: ensure_buffer is tested indirectly via template conformance testing.


def sample_generator():
	"""A small generator with known behaviour to use in the tests."""
	
	yield 27
	yield 42
	yield
	yield "Bob Dole!"


def test_iterruptable():
	iterable = sample_generator()
	
	assert list(interruptable(iterable)) == [27, 42]
	assert next(iterable) == "Bob Dole!"


class TestIterate(object):
	def _do(self, iterable, total=None):
		valid = [
				(True, False, 0, total, 27),
				(False, False, 1, total, 42),
				(False, False, 2, total, None),
				(False, True, 3, total, "Bob Dole!"),
			]
		
		for i, j in enumerate(iterate(iterable)):
			assert j == valid[i], "Element at index " + str(i) + " does not match expected value."
	
	def test_determinate_iterate(self):
		self._do(list(sample_generator()), total=4)
	
	def test_indeterminate_iterate(self):
		self._do(sample_generator())
	
	def test_empty_iterate(self):
		assert list(iterate([])) == []


class TestXMLArgs(object):
	_values = [
			(dict(autocomplete=True), " autocomplete"),  # Truth
			(dict(autocomplete=False), ""),  # Falsy
			(dict(autocomplete=None), ""),  # Falsy
			(dict(autocomplete=""), ""),  # Falsy
			(dict(count=0), ' count="0"'),  # Falsy, but is actually a value.
			(dict(foo=27), ' foo="27"'),  # Stringification.
			(dict(foo_bar=42), ' foo-bar="42"'),  # Hyphenation.
			(dict(ns__bob="dole"), ' ns:bob="dole"'),  # XML namespace notation.
			(dict(class_="first"), ' class="first"'),  # Reserved word avoidance.
			(dict(_omitted="yup"), ""),  # Hide "private" values.
			(dict(class_=['foo', 27, 'bar']), ' class="foo 27 bar"'),  # Non-string iterable support.
			(  # Merged default.
				dict(_source=dict(), placeholder="Bob Dole"),
				' placeholder="Bob Dole"'
			),
			(  # Overridden default.
				dict(_source=dict(placeholder="Placeholder value."), placeholder="Bob Dole"),
				' placeholder="Placeholder value."'
			),
		]
	
	def _do(self, value):
		input, output = value
		assert xmlargs(**input) == output
	
	def test_values(self):
		for test in self._values:
			yield self._do, test


class TestChunker(object):
	_singular_values = [
			('', 'text', "This is some text."),
			('', 'text', "Some text with {matched braces}."),
			('$', '_escape', "Escaped text."),
			('$', '_escape', "Escaped text with {matched brackets}."),
			('#', '_bless', "Blessed text."),
			('&', '_args', "Escaped text."),
			('%', 'format', "Formatted text."),
		]
	
	def _do(self, value):
		token, kind, value = value
		phrase = value if not token else (token + '{' + value + '}')
		
		assert list(chunk(phrase)) == [(kind, value)]
	
	def test_singular_chunks(self):
		for i in self._singular_values:
			yield self._do, i
	
	def test_multiple_chunks(self):
		assert list(chunk("Test ${phrase}.")) == [
				('text', "Test "),
				('_escape', "phrase"),
				('text', ".")
			]
