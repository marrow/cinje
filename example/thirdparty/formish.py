"""Dual (not)declarative form and casting definition.

* Extensive docs.
* Null readme.
* NO i18n.
* 4,299 SLoC, 11.10/6.24=1.78dev
"""

import formish, schemaish, validatish

my_schema = schemaish.Structure()
my_schema.add( 'name', schemaish.String() )
my_schema.add( 'age', schemaish.Integer() )
my_schema == schemaish.Structure("name": schemaish.String(), "age": schemaish.Integer())


class MyStructure(schemaish.Structure):
    name = schemaish.String()
    age = schemaish.Integer()

my_schema = MyStructure()
my_schema == schemaish.Structure("name": schemaish.String(), "age": schemaish.Integer())


form = formish.Form(schema)
form() == '\n<form id="form" action="" class="formish-form" method="post" enctype="multipart/form-data" accept-charset="utf-8">\n\n  <input type="hidden" name="_charset_" />\n  <input type="hidden" name="__formish_form__" value="form" />\n\n<div id="form-name-field" class="field string input">\n\n<label for="form-name">Name</label>\n\n\n<div class="inputs">\n\n<input id="form-name" type="text" name="name" value="" />\n\n</div>\n\n\n\n\n\n</div>\n\n<div id="form-age-field" class="field integer input">\n\n<label for="form-age">Age</label>\n\n\n<div class="inputs">\n\n<input id="form-age" type="text" name="age" value="" />\n\n</div>\n\n\n\n\n\n</div>\n\n\n  <div class="actions">\n      <input type="submit" id="form-action-submit" name="submit" value="Submit" />\n  </div>\n\n</form>\n\n'



def is_string(v):
    """ checks that the value is an instance of basestring """
    if v is None:
        return
    msg = "must be a string"
    if not isinstance(v,basestring):
        raise validatish.Invalid(msg)


class String():
    def __call__(self, v):
        is_string(v)

v = String()


class Widget(object):
	type = None
	template = None
	default_value = ['']

	def __init__(self, **k):
		self.css_class = k.get('css_class', None)
		self.empty = k.get('empty',None)
		self.readonly = k.get('readonly',False)
		self.converter_options = k.get('converter_options', {})
		if not self.converter_options.has_key('delimiter'):
			self.converter_options['delimiter'] = ','


	def to_request_data(self, field, data):
		if data is None:
			return ['']
		string_data = string_converter(field.attr).from_type(data, converter_options=self.converter_options)
		return [string_data]


	def pre_parse_incoming_request_data(self, field, request_data):
		return request_data or self.default_value


	def from_request_data(self, field, request_data):
		string_data = request_data[0]
		if string_data == '':
			return self.empty
		return string_converter(field.attr).to_type(string_data, converter_options=self.converter_options)



class NumberToStringConverter(Converter):
	cast = None
	type_string = 'number'

	def from_type(self, value, converter_options={}):
		if value is None:
			return None
		return str(value)

	def to_type(self, value, converter_options={}):
		if value is None:
			return None
		# "Cast" the value to the correct type. For some strange reason,
		# Python's decimal.Decimal type raises an ArithmeticError when it's
		# given a dodgy value.
		value = value.strip()
		try:
			value = self.cast(value)
		except (ValueError, ArithmeticError):
			raise ConvertError("Not a valid %s"%self.type_string)
		return value


class SimpleSchema(schemaish.Structure):
	email = schemaish.String(validator=schemaish.All(schemaish.NotEmpty, schemaish.Email))
	first_names = schemaish.String(validator=schemaish.NotEmpty)
	last_name = schemaish.String(validator=schemaish.NotEmpty)
	comments = schemaish.String()


def get_form():
	form = formish.Form(SimpleSchema())
	form['comments'].widget = formish.TextArea()
	return form


[
	'formish.forms:Field',  # name, node, attr, form backref
	'formish.forms:Collection:',  #
	'formish.forms:Group',  # collection w/ different template
	'formish.forms:Sequence',  #
	'formish.forms:Form',  # top-level
	'formish.widgets:Widget',  # base
	'formish.widgets:Container',  #
	'formish.widgets:Input',  #
	'formish.widgets:Password',  #
	'formish.widgets:CheckedInput',  # matching fields
	'formish.widgets:CheckedPassword',  # matching fields
	'formish.widgets:Hidden',  #
	'formish.widgets:SequenceDefault',  # min/max, mutable
	'formish.widgets:StructureDefault',  # as per sequence
	'formish.widgets:TextArea',  #
	'formish.widgets:Grid',  #
	'formish.widgets:Checkbox',  #
	'formish.widgets:DateParts',  #
	'formish.widgets:FileUpload',  #
	'formish.widgets:SelectChoice',  #
	'formish.widgets:SelectWithOtherChoice',  #
	'formish.widgets:RadioChoice',  #
	'formish.widgets:CheckboxMultiChoice',  #
	'formish.widgets:CheckboxMultiChoiceTree',  #
	
	'schemaish.attr:Attribute',  # type, title, description, validator
	'schemaish.attr:LeafAttribute',  # default
	'schemaish.attr:String',  #
	'schemaish.attr:Integer',  #
	'schemaish.attr:Float',  #
	'schemaish.attr:Decimal',  #
	'schemaish.attr:Date',  #
	'schemaish.attr:Time',  #
	'schemaish.attr:DateTime',  #
	'schemaish.attr:Boolean',  #
	'schemaish.attr:Container',  #
	'schemaish.attr:Sequence',  #
	'schemaish.attr:Tuple',  #
	'schemaish.attr:Structure',  # dict
	'schemaish.attr:File',  #
	'schemaish.type:File',  #
	
	#'validateish.validate:is_required',  # fail if (none_zero and not v and v != 0) or v is None
	#'validateish.validate:is_string',  # basestring
	#'validateish.validate:is_plaintext',  # [a-zA-Z0-9%s] % extra
	#'validateish.validate:is_integer',  # v != int(v)
	#'validateish.validate:is_number',  # fail if isinstance(v,basestring) or if float(v) fails
	'validateish.validate:is_email',  # regexen!
	'validateish.validate:is_domain_name',  # regex
	'validateish.validate:is_url',  # regex, limited to "^https?://"
	#'validateish.validate:is_equal',  # explicitly allow None, fail if comparison fails
	#'validateish.validate:is_one_of',  # set_of_values, lots of code comments like "what does this do?  why this?"
	#'validateish.validate:has_length',  # min/max
	#'validateish.validate:is_in_range',  # min < value < max
	
	'validateish.validator:Validator',  # abc
	'validateish.validator:CompoundValidator',  # .validators
	#'validateish.validator:Required',  # is_required
	#'validateish.validator:String',  # is_string
	#'validateish.validator:PlainText',  #
	'validateish.validator:Email',  #
	'validateish.validator:DomainName',  #
	'validateish.validator:URL',  #
	#'validateish.validator:Integer',  #
	#'validateish.validator:Number',  #
	#'validateish.validator:Equal',  #
	#'validateish.validator:OneOf',  #
	#'validateish.validator:Length',  #
	#'validateish.validator:Range',  #
	
	'validateish.validator:Any',  #
	'validateish.validator:All',  #
	'validateish.validator:Always',  #
]