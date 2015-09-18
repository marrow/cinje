# encoding: utf-8

"""Application configuration (and command-line interface) toolkit.

* Declarative syntax - neat use.
* Relatively succinct, but still tied to argparse.
* No i18n.
* Docstring docs, few if any comments, real docs.
* Good README, with examples.
* Estimates: 1058 SLoC, 2.55/3.57 p-months, .71 developers.
"""

from __future__ import unicode_literals

from confiture import Confiture
from confiture.schema.containers import many, once
from confiture.schema.containers import Section, Value
from confiture.schema.types import Boolean, Integer, Float, String

# Schema definition:

class UserSection(Section):
	password = Value(String())
	_meta = {'repeat': many, 'unique': True}

class PathSection(Section):
	rate_limit = Value(Float(), default=0)
	enable_auth = Value(Boolean(), default=False)
	user = UserSection()

class VirtualHostSection(Section):
	enable_ssl = Value(Boolean(), default=False)
	path = PathSection()
	_meta = {'repeat': many, 'unique': True}

class MyWebserverConfiguration(Section):
	daemon = Value(Boolean(), default=False)
	pidfile = Value(String(), default=None)
	interface = Value(String(), default='127.0.0.1:80')
	interface_ssl = Value(String(), default='127.0.0.1:443')
	host = VirtualHostSection()


parsed_conf = Confiture(conf, schema=MyWebserverConfiguration()).parse()



types = [
		'confiture.schema.types.Number',  # validates using nubmers.Number ABC, casts using float() - always
		'confiture.schema.types.Integer',  # validate by casting, min/max, cast using int()
		'confiture.schema.types.Float',  # validation by casting only, NO min/max, as per Number
		'confiture.schema.types.Boolean',  # validation via 'value is not True and value is not False', cast with bool()
		'confiture.schema.types.String',  # validates by encoding (thus unicode input, binary output), doesn't cast
		'confiture.schema.types.Regex',  # custom error message, re.match to validate, no cast
		'confiture.schema.types.NamedRegex',  # returns .groupdict() instead of match.string
		'confiture.schema.types.RegexPattern',  # a literal regex pattern, validates by compiling
		'confiture.schema.types.IPAddress',  # uses ipaddr, no cast
		'confiture.schema.types.IPNetwork',  # uses ipaddr, no cast
		'confiture.schema.types.Url',  # validation via urlparse.urlparse()
		'confiture.schema.types.IPSocketAddress',  # handles ip+port gestalts, complex impl, uses ipaddr, no on-disk
		'confiture.schema.types.Eval',  # yes, really; validate by eval with specific globals+locals
	]

# all have default
containers = [
		'confiture.schema.containers.Value',  # scalar value, single type
		'confiture.schema.containers.Choice',  # uses dict, validates key, casts value
		'confiture.schema.containers.List',  # list of scalar values
		'confiture.schema.containers.Array',  # fixed-size list
		'confiture.schema.containers.TypedArray',  # as list, but with elements of a specific type, matching length of schema
		'confiture.schema.containers.Section',  # dict/mapping of sub-section
	]