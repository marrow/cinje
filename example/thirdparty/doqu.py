"""Not quite declarative."""

#Equals  # Compares the value to another value.
#EqualTo  # Compares the values of two fields.
#Exists  # Ensures given field exists in the record.
#Length  # Validates the min/max length of a string.
#NumberRange  # Validates that a number is of a minimum and/or maximum value, inclusive.
Optional  # Allows empty value (i.e. ``bool(value) == False``) and terminates the validation chain (raise StopIteration)
#Required  # Requires that the value is not empty, i.e. ``bool(value)`` returns `True`.
#Regexp  # Validates the field against a user provided regexp.
Email  # Validates an email address. -- BAD REGEX
IPAddress  # Validates an IP(v4) address.  REGEX!
URL  # Simple regexp based url validation.  ARGH!
#Unique   # TBD

AnyOf  # Compares the incoming data to a sequence of valid inputs.
NoneOf  # Compares the incoming data to a sequence of invalid inputs.

email = Email
equals = Equals
equal_to = EqualTo
exists = Exists
ip_address = IPAddress
length = Length
number_range = NumberRange
optional = Optional
required = Required
regexp = Regexp
# TODO: unique = Unique
url = URL
any_of = AnyOf
none_of = NoneOf

class Note(Document):
	structure = {
	    'text': unicode,
	    'is_note': bool,
	}
	defaults = {
	    'is_note': True,
	}
	validators = {
	    'is_note': [AnyOf([True])],
	}
	
	def __unicode__(self):
	    return u'{text}'.format(**self)


class Book(Document):
		title = Field(unicode, required=True, default=u'Hi', label='Title')

class Book(Document):
	structure = {
		'title': unicode
	}
	validators = {
		'title': [validators.Required()]
	}
	defaults = {
		'title': u'Hi'
	}
	labels = {
		'title': u'The Title'
	}

