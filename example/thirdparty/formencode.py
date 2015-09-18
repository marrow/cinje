"""
* Declarative.
* Also not.  It's an old API.
*

* 6,424 SLoC! 16.92/7.32=2.31dev
"""

[
	'formencode.api:Validator',  # base ABC
	'formencode.api:Identity',  # instance of _Identity, nop
	'formencode.api:FancyValidator',  # combines casting and validation, ABC
	
	'formencode.compound:CompoundValidator',  # nests .validators, ABC
	'formencode.compound:Any',  # any()
	'formencode.compound:All',  # all()
	'formencode.compound:Pipe',  # chain(s.validators)
	
	'formencode.foreach:ForEach',  # applies .validators to sequences
	
	#'formencode.validators:ConfirmType',  # subclass/inSubclass/inType/type
	#'formencode.validators:Wrapper',  # allow use of simple casting functions like int/float
	#'formencode.validators:Constant',  # bidirectionally converts to a constant static value
	#'formencode.validators:MaxLength',  #
	#'formencode.validators:MinLength',  #
	#'formencode.validators:NotEmpty',  # empty string, list, etc. not bool(value) and is not 0
	#'formencode.validators:Empty',  #
	#'formencode.validators:Regex',  #
	#'formencode.validators:PlainText',  # regex for [a-zA-Z0-9_-]*
	#'formencode.validators:OneOf',  # value in choices
	'formencode.validators:DictConverter',  # foreign value is the key, native value is the value; act like an enum
	'formencode.validators:IndexListConverter',  # index is foreign value, value is native value
	#'formencode.validators:DateValidator',  # min/max/after now/today or later
	#'formencode.validators:Bool',  # bool()
	#'formencode.validators:RangeValidator',  # min < value < max
	#'formencode.validators:Int',  # int(value)
	#'formencode.validators:Number',  # float(value) or int(value)
	#'formencode.validators:ByteString',  # min/max length, optional encoding
	#'formencode.validators:UnicodeString',  # encoding defaults to utf-8
	#'formencode.validators:Set',  #
	'formencode.validators:Email',  # dual regex, permissive, similar to marrow.mailer's (including DNS)
	'formencode.validators:URL',  # add_http, check will HEAD, allow_idna, require_tld, regexen
	'formencode.validators:XRI',  #
	'formencode.validators:OpenId',  #
	'formencode.validators:FieldStorageUploadConverter',  # traps empty file uploads only
	'formencode.validators:FileUploadKeeper',  #
	'formencode.validators:DateConverter',  # so much regex, so much hardcoded month names
	'formencode.validators:TimeConverter',  # wau
	'formencode.validators:StripField',  # remove key (and associated value) from a mapping
	'formencode.validators:StringBool',  # my normal boolean()
	'formencode.validators:SignedString',  # b64+nonce'd signed string, hardcoded to sha1, does hmac itself!
	#'formencode.validators:IPAddress',  # non-regex, yay!
	#'formencode.validators:CIDR',  # IP or IP/mask
	#'formencode.validators:MACAddress',  #
	'formencode.validators:FormValidator',  # as per Schema, but can continue on errors
	'formencode.validators:RequireIfMissing',  # require a field if another is present or missing
	'formencode.validators:RequireIfPresent',  # (alias)
	#'formencode.validators:FieldsMatch',  # ensure two fields are identical
	'formencode.validators:CreditCardValidator',  # two-field ccType + ccNumber
	'formencode.validators:CreditCardExpires',  # ccExpiresMonth + ccExpiresYear
	'formencode.validators:CreditCardSecurityCode',  # ccType + ccCode
	'formencode.validators:',  #
	
	'formencode.national:DelimitedDigitsPostalCode',  # regex
	'formencode.national:USPostalCode',  #
	'formencode.national:GermanPostalCode',  #
	'formencode.national:FourDigitsPostalCode',  #
	'formencode.national:PolishPostalCode',  #
	'formencode.national:ArgentinaianPostalCode',  #
	'formencode.national:CanadianPostalCode',  #
	'formencode.national:UKPostalCode',  #
	
	'formencode.national:CountryValidator',  # Full Name to ISO short-form.
	'formencode.national:PostalCodeInCountryFormat',  # given an ISO short country, figure out the postal format
	'formencode.national:USStateProvince',  # only does states
	'formencode.national:USPhoneNumber',  # regex
	'formencode.national:InternationalPhoneNumber',  # lots and lots of regex
	'formencode.national:LanguageValidator',  # long name to ISO short-form.
	
	'formencode.schema:Schema',  # FancyValidator using declarative dictionary key to validator mappings.
	'formencode.schema:SimpleFormValidator',  #
]

# All FancyValidators take:
# if_empty (value to use if evaluates to false, but isn't 0 or False)
# not_empty ("required")
# strip (obvious)
# if_invalid (don't raise Invalid, return this if it's invalid on .to_python)
# if_invalid_python (as above, but for .from_python)
# accept_python (True by default, don't validate .from_python using _validate_python and _validate_other)
