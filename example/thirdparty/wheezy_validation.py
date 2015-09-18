# encoding: utf-8

"""A library primarily for the validation of form and model data.

* Non-declarative syntax.
* Relatively succinct.
* Utterly fails at the included regular expressions.
* I18n
* Sphinx docs
* Trivial README (installation + links to other sources of info)
* Estimates: 1,830 SLoC, 4.53/4.44 p-months, 1.02 developers
"""

# From the wheezy.validation user guide:

credential_validator = Validator({
	'username': [required, length(max=10)],
	'password': [required, length(min=8, max=120)]
})

user = {'username': '', 'password': ''}
errors = {}
success = credential_validator.validate(user, errors)

# success(bool) - True if validation succeeded, False otherwise
# user - sample data being validated
# credential_validator - concrete instance of the validation schema
# errors - dictionary modified to add failure messages


rules = dict(
		#ignore = 'wheezy.validation.rules.IgnoreRule',  # pass if True
		#required = 'wheezy.validation.rules.RequiredRule',  # pass if bool(value) is True
		#not_none = 'wheezy.validation.rules.NotNoneRule',  # pass if value is not None
		#missing = 'wheezy.validation.rules.RequiredRule',  # pass if bool(value) is False
		#empty = 'wheezy.validation.rules.RequiredRule',  # pass if bool(value) is False
		#length = 'wheezy.validation.rules.LengthRule',  # pass if min < len(value) < max
		#compare = 'wheezy.validation.rules.CompareRule',  # equal/not_equal, pass if condition matches
		#predicate = 'wheezy.validation.rules.PredicateRule',  # fail if bool(predicate(instance)) is False
		#must = 'wheezy.validation.rules.ValuePredicateRule',  # fail if bool(predicate(value)) is False
		#range = 'wheezy.validation.rules.RangeRule',  # pass if min < value < max
		
		# Advanced (or simply expensive) predicates.
		#regex = 'wheezy.validation.rules.RegexRule',  # pass if re.match(regex, value); optionally 'negated'
		#one_of = 'wheezy.validation.rules.OneOfRule',  # pass if value in choices
		
		# Superfluous additional built-in predicates.
		slug = 'wheezy.validation.rules.SlugRule',  # regex; [a-zA-Z0-9_-]+
		email = 'wheezy.validation.rules.EmailRule',  # bad regex; can't handle name+tag@domain.tld or new TLDs
		scientific = 'wheezy.validation.rules.ScientificRule',  # regex for sci. notation numbers
		base64 = 'wheezy.validation.rules.Base64Rule',  # regex
		urlsafe_base64 = 'wheezy.validation.rules.URLSafeBase64Rule',  # regex
		
		# Combantorial meta-prdicates.
		and_ = 'wheezy.validation.rules.AndRule',  # evaluate all, regardless of individual failures
		or_ = 'wheezy.validation.rules.OrRule',  # pass if any(rules) pass; failures ignored unless all fail
		iterator = 'wheezy.validation.rules.IteratorRule',  # apply rules iteratively; pass if all(rule(i) for i in value)
		
		# Date-specific predicates.  This is just silly.
		relative_date = 'wheezy.validation.rules.RelativeDateDeltaRule',
		relative_utcdate = 'wheezy.validation.rules.RelativeUTCDateDeltaRule',
		relative_tzdate = 'wheezy.validation.rules.RelativeTZDateDeltaRule',
		relative_datetime = 'wheezy.validation.rules.RelativeDateTimeDeltaRule',
		relative_utcdatetime = 'wheezy.validation.rules.RelativeUTCDateTimeDeltaRule',
		relative_tzdatetime = 'wheezy.validation.rules.RelativeTZDateTimeDeltaRule',
		relative_timestamp = 'wheezy.validation.rules.RelativeUnixTimeDeltaRule',
		relative_unixtime = 'wheezy.validation.rules.RelativeUnixTimeDeltaRule',
		
		# Typecasting predicates.
		adapter = 'wheezy.validation.rules.AdapterRule',
		int_adapter = 'wheezy.validation.rules.IntAdapterRule',
	)

