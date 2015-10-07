# encoding: utf-8

from __future__ import unicode_literals

from cinje.util import Line, bytes, str


def test_line_processing():
	assert Line(None, "Some text.").kind == 'text'
	assert Line(None, "# Comment?").kind == 'comment'
	assert Line(None, ": pass").kind == 'code'


def test_line_formatting():
	assert Line(None, "\tHuzzah?").stripped == "Huzzah?"
	assert Line(None, "foo bar baz").partitioned == ('foo', 'bar baz')
	assert repr(Line(1, "First!")) == 'Line(1, text, "First!")'
	assert str(Line(None, "Flat.")) == "Flat."
	assert str(Line(None, "Indented.", 1)) == "\tIndented."
	assert bytes(Line(None, "Text.")) == b"Text."


def test_line_clone():
	line = Line(27, "\t\tMy test line!", 2)
	clone = line.clone(line="New line.")
	
	assert line.number == clone.number
	assert line.line != clone.line
	assert line.scope == clone.scope
	assert str(clone) == '\t\tNew line.'
