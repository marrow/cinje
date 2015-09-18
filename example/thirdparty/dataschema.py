# encoding: utf-8

"""Python data structure schema validation.  Based on jsonschema.

* Non-declarative syntax; nested standard types.
* Extremely limited; despite quite complete tests.  (And interesting test structure!)
* So limited that all base types are built-in as methods of a monolithic class.
* Interesting use syntax; pure validation.  Code confirms all logic in single monolithic class.
* No i18n.
* No docstrings, few if any comments (mostly commented out print *statements*), tests-as-documentation.
* Mediocre README, only has consumption (not production) example.
* Single. Monolithic. Module.  (But a package for a single test module.)
* Estimates: 493 SLoC
* Style guide: Dr. Dobb's Eye-Bleed
"""

from __future__ import unicode_literals

# From the tests:

schema = {
	"type": str,
	"pattern": "^[0-9]{0,10}$"
}

base_1 = {
		"type": dict,
		"items": {
			"this": {"type": str}
			}
	}

base_2 = {
		"type": dict,
		"items": {
			"that": {"type": str}
			}
	}

list_of_base_schema = {
		"type": list,
		"items": {
			"type": dict,
			"extends": ["the_first_base_schema", "the_second_base_schema"],
			"additionalItems": {"type": "any"}
			}
	}

validator = dataschema.Validator(
		list_of_base_schema,
		other_schemata={
			"the_first_base_schema" : base_1,
			"the_second_base_schema": base_2,
			}
		)


# validator.validate(instance)


# Roughly from the readme:

data = json.load(some_file)
errors = dataschema.Validator(my_schema).validate(data)
if errors:
	pass  # freak out
else:  # <- sic
	pass  # do stuff
