# encoding: utf-8

from cinje.util import Lines


class TestLines(object):
	"""Lines is mostly a pass-through to the underlying buffer deque.
	
	We group these tests together.
	"""
	
	@property
	def example(self):
		return Lines("text\nmore text\nreplacement ${text}\n: code\n\n# comment\n")
	
	def test_representation(self):
		assert repr(self.example) == 'Lines(7)'
	
	# TODO: Make this a fixture variant of example and repeat all tests on it instead of... this.
	def test_load_from_filelike(self):
		text = str(self.example).split('\n')
		
		class MockFile(object):
			def readlines(self):
				return text
		
		self.test_basic_usage(Lines(MockFile()))
		self.test_iteration_methods(Lines(MockFile()))
	
	def test_empty_buffer(self):
		example = Lines()
		
		assert len(example) == example.count == len(example.buffer) == 0
	
	def test_basic_usage(self, example=None):
		example = example if example else self.example
		
		assert len(example) == example.count == len(example.buffer) == 7
		assert str(example.peek()) == 'text'
		assert str(example.next()) == 'text'
		assert len(example) == example.count == len(example.buffer) == 6
		example.reset()
		assert len(example) == example.count == len(example.buffer) == 7
		list(example)
		assert len(example) == example.count == len(example.buffer) == 0
		example.push("Test.")
		assert len(example) == example.count == len(example.buffer) == 1
		assert str(example) == "Test."
		assert len(example) == example.count == len(example.buffer) == 0
		example.push("Also.")
		assert len(example) == example.count == len(example.buffer) == 1
		assert str(example) == "Also."
		assert len(example) == example.count == len(example.buffer) == 0
		example.append("Again.")
		assert len(example) == example.count == len(example.buffer) == 1
		assert str(example) == "Again."
		assert len(example) == example.count == len(example.buffer) == 0
	
	def test_iteration_methods(self, example=None):
		example = example if example else self.example
		
		assert str(example.next()) == 'text'
		assert str(next(example)) == 'more text'
		assert str(next(iter(example))) == 'replacement ${text}'
		assert str(example) == 'code\n\n# comment\n'
		assert len(example) == 0
		example.reset()
		assert str(next(example)) == 'text'
