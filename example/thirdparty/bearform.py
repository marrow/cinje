# encoding: utf-8

"""It's forms… and a near-complete duplication of bearfield.

It's such a duplicate you can just look in the bearfield.py example for the defined types.

* Declarative syntax.
* Relatively succinct.
* No i18n.
* Serious type inference.
* Reasonable README, though the README is the only source of example use and is not included in the distribution.
* Estimates: 904 SLoC, 2.16/3.35 p-months, 0.64 developers.
"""

from __future__ import unicode_literals

from bearform import Form, Field


class BearForm(Form):
	name = Field(str)
	type = Field(str)
	height = Field(float)


bear = BearForm.decode(data)  # data is a JSON dict structure
bear.validate()

bear.encode()  # returns JSON-safe dict structure
bear.to_dict()  # as expected
bear.to_obj(thing)  # setattr() on thing



from bearform import ValidationError

def is_not_empty(cls, name, value):
	if not value:
		raise ValidationError("{} cannot be empty".format(name))

def is_positive(cls, name, value):
	if value <= 0:
		raise ValidationError("{} must be a positive value".format(name))

class BearForm(Form):
	name = Field(str, validators=[is_not_empty])
	type = Field(str)
	height = Field(float, validators=[is_positive])
