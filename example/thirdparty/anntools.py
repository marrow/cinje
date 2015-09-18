# encoding: utf-8

"""A set of Python 3 function annotation tools supporting Python 2.4 and up.

* Non-declarative syntax.  (Decorators or annotations.)
* Relatively succinct.
* No i18n.
* Docstring docs.
* Trivial README (effectively one paragraph and a non-project-specific link.)
* Estimates: 2,057 SLoC, 5.12/4.65 p-months, 1.10 developers.
* Last commit: Aug 2008
* Last release: 0.5.1 (alpha) June 2008

Has nifty "Cooperation" feature that the documentation utterly fails to describe in purpose, intent, implementation,
or use.

Double API; _check class method and check instance method.  This means a *lot* of duplicated code.
"""

from __future__ import unicode_literals


# From the wiki: https://code.google.com/p/anntools/wiki/

# Validation

from anntools.validation import *

@validate(Unicode, n=Int)
def myfunc(n):
	"""Python 2 example."""
	return '#' * n

# @validate
# def myfunc(n: Int) -> Str:
# 	"""Python 3 example."""
# 	return b'#' * n


# Conversion

from anntools.conversion import *

@convert(AsFloat, n=AsInt)
def square(n):
	return n * n

# @convert
# def square(n: AsInt) -> AsFloat:
# 	return n * n


# Type Checking

from anntools.typecheck import *

@typecheck(unicode, n=int)
def myfunc(n):
	return '#' * n



validators = dict(
		abc = 'anntools.validation.Validator',  # abstract base
		
		# Meta predicates.
		and_ = 'And',  # stops evaluating on first failure
		or_ = 'Or',  # stops evaluating on first success
		not_ = 'Not',  # inverts wrapped validator
		
		none = 'AllowNone',  # pass if value is None
		
		# Basic types.
		Bool = 'Bool',  # isinstance(value, bool)
		Int = 'Int',  # isinstance(value, Int) and min < value < max
		Float = 'Float',  # isinstance(value, (int, float)) and not isinstance(value, bool) and min < value < max
		Complex = 'Complex',  # isinstance(value, complex)
		Tuple = 'Tuple',  # isinstance(value, tuple)
		List = 'List',  # isinstance(value, list)
		Dict = 'Dict',  # isinstance(value, dict)
		Set = 'Set',  # isinstance(value, set)
		
		# Python 2.x
		Str = 'Str',  # isinstance(value, str) and len(value) < maxlen
		Unicode = 'Unicode',  # isinstance(value, unicode) and len(value) < maxlen
		Bytes = 'Bytes',  # compat, subclasses Str
		
		# Python 3.x
		# Str = 'Str',  # isinstance(value, str) and len(value) < maxlen
		# Unicode = 'Str',  # compat, subclasses Str
		# Bytes = 'Bytes',  # isinstance(value, bytes) and len(value) < maxlen
		
		# Generic
		
		InstanceOf = 'InstanceOf',  # isinstance(value, cls)
		SubclassOf = 'SubclassOf',  # type(value) is classtype and issubclass(value, cls)
	)



transforms = dict(
		abc = 'anntools.conversion.Converter',  # abstract base
		
		# These all also handle "allow_none" testing.
		AsBool = 'anntools.conversion.AsBool',  # bool(value)
		AsInt = 'AsInt',  # int(value)
		AsFloat = 'AsFloat',  # float(value)
		
		# 2.x
		AsStr = 'AsStr',  # value (if str) or value.encode('utf8') (if unicode) else str(value)
		AsUnicode = 'AsUnicode',  # value (if unicode) or value.decode('utf8') (if str) else ujnicode(value)
		AsBytes = 'AsStr',  # compat
		
		# 3.x
		# AsBytes = '',  # as per AsStr
		# AsStr = '',  # as per AsUnicode
		# AsUnicode = 'AsStr',  # compat
	)
