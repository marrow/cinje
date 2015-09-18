# encoding: utf-8

"""Python data structure schema validation.  Based on jsonschema.

* Declarative-ish syntax.
* Hey, yo, oy, it's I18N, for reals.
* Estimates: 4,436 SLoC, 11.47/6.32 p-months, 1.82 developers
"""

from __future__ import unicode_literals


# - Define a schema
# - Create a form object.
# - Assign non-default widgets to fields in the form (optional).
# - Render the form.


import colander

class Person(colander.MappingSchema):
	name = colander.SchemaNode(colander.String())
	age = colander.SchemaNode(colander.Integer(),
							  validator=colander.Range(0, 200))

class People(colander.SequenceSchema):
	person = Person()

class Schema(colander.MappingSchema):
	people = People()

schema = Schema()


from deform import Form
myform = Form(schema, buttons=('submit',))

form = myform.render([data][, readonly=True])

controls = request.POST.items() # get the form controls

try:
	appstruct = myform.validate(controls)  # call validate
except ValidationFailure, e: # catch the exception
	return {'form':e.render()} # re-render the form with an exception

# the form submission succeeded, we have the data
return {'form':None, 'appstruct':appstruct}




default_widget_makers = {
	colander.Mapping: widget.MappingWidget,
	colander.Sequence: widget.SequenceWidget,
	colander.String: widget.TextInputWidget,
	colander.Integer: widget.TextInputWidget,
	colander.Float: widget.TextInputWidget,
	colander.Decimal: widget.TextInputWidget,
	colander.Boolean: widget.CheckboxWidget,
	colander.Date: widget.DateInputWidget,
	colander.DateTime: widget.DateTimeInputWidget,
	colander.Tuple: widget.TextInputCSVWidget,
	colander.Money: widget.MoneyInputWidget,
	colander.Set: widget.CheckboxChoiceWidget,
}

[
	'deform.schema.FileData',
	'deform.widget.AutocompleteInputWidget',
	'deform.widget.TextAreaWidget',
	'deform.widget.RichTextWidget',
	'deform.widget.PasswordWidget',
	'deform.widget.HiddenWidget',
	'deform.widget.OptGroup',
	'deform.widget.SelectWidget',
	'deform.widget.Select2Widget',
	'deform.widget.RadioChoiceWidget',
	'deform.widget.CheckedInputWidget',
	'deform.widget.CheckedPasswordWidget',
	'deform.widget.FormWidget',
	'deform.widget.FileUploadWidget',
	'deform.widget.DatePartsWidget',
	'deform.widget.TextAreaCSVWidget',
	'deform.widget.ResourceRegistry',
]


widget = dict(hidden=False, readonly=False, category="default|leaf-level|structural", error_class, css_class, item_css_class, style, requirements)

