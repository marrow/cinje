# encoding: utf-8

from cinje.util import fragment, flatten


class TestBasicFormatters(object):
	def test_formatted_strings(self):
		assert flatten(fragment('%{"{foo}" foo=27}')()) == '27\n'
		assert flatten(fragment('%{"{0}" 27}')()) == '27\n'
		assert flatten(fragment('%{format 27}', format="{0}")()) == '27\n'
		assert flatten(fragment('%{format() 27}', format=lambda: "{0}")()) == '27\n'
		assert flatten(fragment('%{format["first"] 27}', format=dict(first="{0}"))()) == '27\n'
		assert flatten(fragment('%{format[0] 27}', format=["{0}"])()) == '27\n'
	
	def test_basic_text(self):
		assert flatten(fragment('text')()) == "text\n"
	
	def test_escaped_text(self):
		assert flatten(fragment('${"27"}')()) == "27\n"
		assert flatten(fragment('${"<html>"}')()) == "&lt;html&gt;\n"
		
	def test_blessed_text(self):
		assert flatten(fragment('#{"42"}')()) == "42\n"
		assert flatten(fragment('#{"<html>"}')()) == "<html>\n"
	
	def test_json_object(self):
		assert flatten(fragment('@{[27,42]}')()) == "[27, 42]\n"
