# encoding: utf-8

from __future__ import unicode_literals

from marrow.dsl.base import Classifier


class CinjeScopeClassifier(Classifier):
	"""Mark and clean up end-of-scope lines.
	
	Scopes are increased via block translators, decreased via explicit ": end".
	"""
	
	priority = -1010
	
	def classify(self, context, line):
		text = line.stripped
		
		if not text:
			return
		
		if text[0] != ':':
			return
		
		if text[1:].strip() != 'end':
			return
		
		line.line = line.stripped = ''
		line.tag.add('_end')
		context.input.scope -= 1


class CinjeLineClassifier(Classifier):
	"""Classify lines into three broad groups: text, code, and comments."""
	
	priority = -1000
	
	def classify(self, context, line):
		text = line.stripped
		
		if not text:
			line.tag.add('blank')
			line.line = ''  # Blank lines are really blank.
			return
		
		if text[0] == ':':
			text = line.line = line.stripped = text[1:].strip()  # Code in cinje acquires scope through other means.
			line.tag.add('code')
			
			if not text:
				line.tag.add('blank')
				return
			
			if text[0] == '@':
				line.tag.add('decorator')
				return
			
			identifier, _, body = text.partition(' ')
			
			if identifier in ('from', 'import'):
				line.tag.add('import')
			elif identifier in ('def', ):  # TODO: Query valid block handlers.
				line.tag.add(identifier)
		
		# TODO: Extract relevant parts as "CommentClassifier", add to cinje namespace.
		elif text[0] == '#' and not text.startswith("#{"):
			line.line = text  # Eliminate extraneous whitespace and match overall scope.
			line.tag.add('code')
			line.tag.add('comment')
			
			if 'coding:' in text:
				line.tag.add('encoding')
		
		else:
			line.tag.add('text')
