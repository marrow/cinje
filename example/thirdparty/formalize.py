# 832 SLoC

v = FormValidator(
	firstname=Unicode(),
	surname=Unicode(required="Please enter your surname"),
	age=Int(greaterthan(18, "You must be at least 18 to proceed"), required=False),
)

input_data = {
   'firstname': u'Fred',
   'surname': u'Jones',
   'age': u'21',
}
v.process(input_data) == {'age': 21, 'firstname': u'Fred', 'surname': u'Jones'}


input_data = {
   'firstname': u'Fred',
   'age': u'16',
}
v.process(input_data)  # raises ValidationError
# ValidationError([('surname', 'Please enter your surname'), ('age', 'You must be at least 18 to proceed')])


#assert_true  # raise if not value
#assert_false  # raise if value
#test  # raise if callback(value)
#minlen
#maxlen
#greaterthan
#lessthan
#notempty
#matches  # regex
#equals
#is_in
looks_like_email  # basic, but kudos for not using a regex!
maxwords
minwords


CustomType  # for subclassing
PassThrough  # return value
Int  # int(value) or raise ValidationError
Float  # as Int
Decimal  # as Int
Unicode  # optionally strip, unicode(value), no encoding
Bool  # default (undefined) is False by default

Calculated  # return callback(*source_fields)

DateTime
Date
