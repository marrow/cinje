# encoding: utf-8

import pytest
from cinje.util import fragment, flatten



def std():
	from cinje.std import html as std
	return std


# {None: 'text', '${': '_escape', '#{': '_bless', '&{': '_args', '%{': 'format', '@{': '_json'}

class TestNotImplementedFormatters(object):
	def test_formatted_string(self):
		with pytest.raises(NotImplementedError):
			fragment('%{"{foo}" foo=27}')
		
		with pytest.raises(NotImplementedError):
			fragment('%{"{0}" 27}')
		
		with pytest.raises(NotImplementedError):
			fragment('%{format 27}', format="{0}")
		
		with pytest.raises(NotImplementedError):
			fragment('%{format() 27}', format=lambda: "{0}")
		
		with pytest.raises(NotImplementedError):
			fragment('%{format["first"] 27}', format=dict(first="{0}"))
		
		with pytest.raises(NotImplementedError):
			fragment('%{format[0] 27}', format=["{0}"])


class TestBasicFormatters(object):
	def test_basic_text(self):
		assert flatten(fragment('text')()) == "text\n"
	
	def test_escaped_text(self):
		assert flatten(fragment('${"27"}')()) == "27\n"
		assert flatten(fragment('${"<html>"}')()) == "&lt;html&gt;\n"
		
	def test_blessed_text(self):  # FIXME: These can't start at the beginning of lines due to priority...
		assert flatten(fragment('text #{"42"}')()) == "text 42\n"
		assert flatten(fragment('text #{"<html>"}')()) == "text <html>\n"
	
	def test_json_object(self):
		assert flatten(fragment('@{[27,42]}')()) == "[27, 42]\n"
