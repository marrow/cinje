[
	'formular.fields:Field',  # ABC; required, requires, equals, default, widget
	'formular.fields:Mapping',  #
	'formular.fields:SizedField',  # min/max
	
	'formular.fields:TextField',  #
	'formular.fields:PasswordField',  #
	'formular.fields:ComparableField',  #
	'formular.fields:NumberField',  #
	'formular.fields:IntegerField',  #
	'formular.fields:FloatField',  #
	'formular.fields:DecimalField',  #
	'formular.fields:BooleanField',  #
	'formular.fields:SubmitField',  #
	'formular.fields:ChoiceField',  #
	'formular.fields:MultiChoiceField',  # list
	'formular.fields:Multiple',  # min/max len, list
	'formular.fields:Separated',  # separator, strip
	'formular.fields:ReCAPTCHAField',  #
	
	# Babel dependency
	'formular.fields:TimeField',  #
	'formular.fields:DateField',  #
	
	'formular.forms:Form',  #
	'formular.forms:HTMLForm',  #
	'formular.forms:ConfigurationForm',  #
	
	#'formular.validators:required',  # bool(value)
	#'formular.validators:requires',  # form.fields[name].value if value else fail
	#'formular.validators:equals',  # form.fields[name].value == value
	#'formular.validators:min_length',  #
	#'formular.validators:max_length',  #
	#'formular.validators:min_value',  #
	#'formular.validators:max_value',  #
	'formular.validators:is_email',  # regexen! BAD REGEXEN!
	
	'formular.widgets:*',  # lots and lots, all tied to field types
]


class LoginForm(Form):
	username = TextField(label=u"Username", required=True)
	password = PasswordField(label=u"Password", required=True)
	repeat_password = password.copy(label=u"Repeat password",
									equals="password")
	permanent = BooleanField(label=u"Keep me logged in")

