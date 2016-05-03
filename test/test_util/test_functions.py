# encoding: utf-8

from cinje.util import interruptable, iterate, xmlargs, chunk, ensure_buffer, Line, strip_tags

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
	assert list(iterable) == ["Bob Dole!"]


def test_ensure_buffer():
	class context(object):
		flag = {'buffer'}
	
	assert 'text' not in context.flag
	result = list(ensure_buffer(context))
	assert 'text' in context.flag
	assert len(result) > 0
	assert isinstance(result[0], Line)
	
	result = list(ensure_buffer(context))
	assert len(result) == 0


def test_html_stripper():
	assert strip_tags('<foo>bar</foo>') == 'bar'


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
	def _do(self, value):
		input, output = value
		assert xmlargs(**input) == output
	
	def test_valueless_attribute(self):
		self._do((dict(autocomplete=True), " autocomplete"))
	
	def test_falsy_value_exclusion(self):
		self._do((dict(autocomplete=False), ""))
		self._do((dict(autocomplete=None), ""))
		self._do((dict(autocomplete=""), ""))
	
	def test_falsy_zero_exception(self):
		self._do((dict(count=0), ' count="0"'))
	
	def test_value_stringification(self):
		self._do((dict(foo=27), ' foo="27"'))
	
	def test_key_hyphenation(self):
		self._do((dict(foo_bar=42), ' foo-bar="42"'))
	
	def test_xml_namespace(self):
		self._do((dict(ns__bob="dole"), ' ns:bob="dole"'))
	
	def test_reserved_word_avoidance(self):
		self._do((dict(class_="first"), ' class="first"'))
	
	def test_exclude_private_keys(self):
		self._do((dict(_omitted="yup"), ""))
	
	def test_iterable_support(self):
		self._do((dict(class_=['foo', 27, 'bar']), ' class="foo 27 bar"'))
	
	def test_defaults_merged(self):
		self._do((
				dict(_source=dict(), placeholder="Bob Dole"),
				' placeholder="Bob Dole"'
			))
	
	def test_defaults_overridden(self):
		self._do((
				dict(_source=dict(placeholder="Placeholder value."), placeholder="Bob Dole"),
				' placeholder="Placeholder value."'
			))


class TestChunker(object):
	def _do(self, value):
		token, kind, value = value
		phrase = value if not token else (token + '{' + value + '}')
		
		result = next(chunk(Line(0, phrase)))
		assert result.number == 0
		assert result.line == value
		assert result.kind == kind
	
	def test_plain_text_chunk(self):
		self._do(('', 'text', "This is some text."))
	
	def test_plain_text_matched_braces(self):
		self._do(('', 'text', "Some text with {matched braces}."))
	
	def test_escaped_text_chunk(self):
		self._do(('$', 'escape', "Escaped text."))
	
	def test_excaped_text_matched_braces(self):
		self._do(('$', 'escape', "Escaped text with {matched brackets}."))
	
	def test_blessed_text_chunk(self):
		self._do(('#', 'bless', "Blessed text."))
	
	def test_argument_chunk(self):
		self._do(('&', 'args', "Arguments."))
	
	def test_formatted_chunk(self):
		self._do(('%', 'format', "Formatted text."))
	
	def test_multiple_chunks(self):
		parts = list(chunk(Line(0, "Test ${phrase}.")))
		
		assert parts[0].kind == 'text'
		assert parts[0].line == 'Test '
		assert parts[1].kind == 'escape'
		assert parts[1].line == 'phrase'
		assert parts[2].kind == 'text'
		assert parts[2].line == '.'

