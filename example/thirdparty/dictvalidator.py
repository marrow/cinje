# encoding: utf-8

"""Validate dictionary structures... we think.

* Declarative syntax.
* Barely any code.
* No i18n.
* Estimates: 112...
"""

from __future__ import unicode_literals

from dictvalidator import DictValidator
from dictvalidator.fields import Field, ArrayField, StructuredDictField



class Foo(DictValidator):
	foo = Field(str, required=True)


Foo({'foo': "bar"}) # raises on failure... things are being smoked, and I want some
