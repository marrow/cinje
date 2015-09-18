# encoding: utf-8

"""Another MongoDB ODM.

* Declarative syntax.
* Relatively succinct.
* No i18n.
* Serious type inference.
* Reasonable README, though the README is the only source of example use and is not included in the distribution.
* Estimates: 1,214 SLoC, 2.94/3.77 p-months, 0.78 developers.
"""

from __future__ import unicode_literals

from bearfield import connection
from bearfield import Document, Field


connection.add('example', 'mongodb://localhost/example')


class Bear(Document):
	class Meta:
		connection = 'example'
	
	name = Field(str)
	type = Field(str)
	height = Field(float)


bear = Bear(name='timmy', type='grizzly', height='9.8')
bear.save()


types = dict(
		abc = 'bearfield.types.FieldType',  # abstract base
		
		#builtin = 'BuiltinType',  # special casing for unicode, builtin(value)
		
		# Date handling
		#date = 'DateType',  # expands date() into datetime(), converts back later
		#datetime = 'DateTimeType',  # time(0) expansion and typechecking… mostly typechecking
		#time = 'TimeType',  # date(epoch, time) expansion and typechecking
		
		document = 'DocumentType',  # Handle descent into a child document.
		list = 'ListType',  # capable of handling non-list list-likes
		set = 'SetType',  # same as list, stores as list internally
		dict = 'DictType',  # same as list, stores as OrderedDict internally
	)
