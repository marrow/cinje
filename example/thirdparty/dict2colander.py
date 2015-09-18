# encoding: utf-8

"""Does what it says.

* The opposite of declarative.
* No i18n.
* Estimates: 446 SLoC
* Docs excluded from package.
"""

from __future__ import unicode_literals


# Normal
import colander

class Person(colander.MappingSchema):
	name = colander.SchemaNode(colander.String())
	age = colander.SchemaNode(colander.Int(),
							  validator=colander.Range(0, 200))

	@colander.instantiate()
	class phones(colander.SequenceSchema):

		@colander.instantiate()
		class phone(colander.MappingSchema):
			location = colander.SchemaNode(colander.String(),
								 validator=colander.OneOf(['home', 'work']))
			number = colander.SchemaNode(colander.String())


# Dictmode
from dict2colander import dict2colander

schema_dict = {
	'type': 'Mapping',
	'name': 'person',
	'subnodes': [
		{'type': 'String', 'name': 'name'},

		{'type': 'Integer', 'name': 'age',
		 'validators':
			{'Range': {'args': ('0', '200')}}},

		{'type': 'Sequence',
		 'name': 'phones',
		 'subnodes': [

			 {'type': 'Mapping', 'name': 'phone',
			  'subnodes': [

				  {'type': 'String', 'name': 'location',
				   'validators':
					 {'OneOf': {'args': (['home', 'work'],)}}},

				  {'type': 'String', 'name': 'number'}

			  ]}]},
	]
}

schema = dict2colander(schema_dict)
data = {
		 'name': 'keith',
		 'age': '20',
		 'friends':[('1', 'jim'),('2', 'bob'), ('3', 'joe'), ('4', 'fred')],
		 'phones':[{'location':'home', 'number':'555-1212'},
				   {'location':'work', 'number':'555-8989'},],
		 }

serialized_data = schema.deserialize(data)
print serialized_data


# Yaml version of that schema
"""
---
name: person
type: Mapping

subnodes:
	- name: name
	  type: String

	- name: age
	  type: Integer
	  validators:
		Range:
			args: ['0', '200']

	- name: phones
	  type: Sequence
	  subnodes:
		- name: phone
		  type: Mapping
		  subnodes:
			- name: location
			  type: String
			  validators:
				OneOf:
					args: [[home, work]]

			- name: number
			  type: String
"""

# Sample record
"""
---
name: keith
age: 20
friends:
	- [1, jim]
	- [2, bob]
	- [3, joe]
	- [4, fred]

phones:
	- location: home
	  number: 555-1212

	- location: work
	  number: 555-8989
"""


# Use

import yaml
import dict2colander

def deserialize(yaml_doc, yaml_schema):
	mapping_schema = dict2colander.dict2colander(yaml_schema)
	return mapping_schema.deserialize(yaml_doc)

f = open('doc.yaml')
doc = yaml.load(f)
f.close()

f = open('schema.yaml')
schema = yaml.load(f)
f.close()

dict_doc = deserialize(doc, schema)
print dict_doc


#

self.add_type('Mapping', colander.Mapping)
self.add_type('Sequence', colander.Sequence)
self.add_type('Tuple', colander.Tuple)
self.add_type('Integer', colander.Integer)
self.add_type('Float', colander.Float)
self.add_type('String', colander.String)
self.add_type('Decimal', colander.Decimal)
self.add_type('Boolean', colander.Boolean)
self.add_type('DateTime', colander.DateTime)
self.add_type('Date', colander.Date)
self.add_type('Time', colander.Time)

#self.add_validator('Range', colander.Range, RangeArgsSchema)
#self.add_validator('Length', colander.Length, LengthArgsSchema)
#self.add_validator('OneOf', colander.OneOf, OneOfArgsSchema)
#self.add_validator('Regex', colander.Regex, RegexArgsSchema)
self.add_validator('Email', colander.Email, EmailArgsSchema)

