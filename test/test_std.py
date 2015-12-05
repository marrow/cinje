# encoding: utf-8

import pytest
from cinje.util import flatten



@pytest.fixture
def std():
	from cinje.std import html as std
	return std


class TestStandardHTMLFive(object):
	def test_div(self, std):
		assert flatten(std.div(foo="bar", data_baz="42")) == '<div data-baz="42" foo="bar">\n</div>\n'
	
	def test_span(self, std):
		assert flatten(std.span("Hello!")) == '<span>Hello!</span>'
	
	def test_span_iterator(self, std):
		assert flatten(std.span(iter(["Yay!"]))) == '<span>Yay!</span>'
	
	def test_span_protected(self, std):
		assert flatten(std.span("<malicious>")) == '<span>&lt;malicious&gt;</span>'
	
	def test_link(self, std):
		assert flatten(std.link('http://example.com')) == '<a href="http://example.com"></a>'
	
	def test_heading(self, std):
		assert flatten(std.heading('Allo.')) == '<h1>Allo.</h1>\n'
	
	def test_heading_iterator(self, std):
		assert flatten(std.heading(iter(['Wazzit.']), 2)) == '<h2>Wazzit.</h2>\n'
