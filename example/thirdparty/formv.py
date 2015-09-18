[
	#'formv.validators.base:VBase',  # ABC; reqiured, strip
	#'formv.validators.base:VConstant',  #
	#'formv.validators.base:VBool',  # bool(value)
	#'formv.validators.base:VEmpty',  #
	#'formv.validators.base:VLength',  # min/max
	#'formv.validators.base:VRange',  # min < val < max
	#'formv.validators.base:VList',  # isinstance(list) or isinstance(set, tuple), returns value, list(value), or [value]
	#'formv.validators.base:VSet',  # as per VList, but with sets
	
	#'formv.validators.chained:VAnyField',  # at least one field specified has a value
	#'formv.validators.chained:VAllFields',  #
	#'formv.validators.chained:VPair',  # if a has a value, b must have value too
	'formv.validators.chained:VCountryPostcode',  #
	'formv.validators.chained:VCountryStatePostcode',  #
	'formv.validators.chained:VPostcodeFormat',  #
	'formv.validators.chained:VState',  #
	'formv.validators.chained:VCurrency',  #
	'formv.validators.chained:VLanguage',  #
	'formv.validators.chained:VGeoDistance',  #
	'formv.validators.chained:VPhoneFormat',  #
	'formv.validators.chained:VCreditCard',  #
	
	#'formv.validators.compound:VCompound',  # .validators
	#'formv.validators.compound:VAny',  # return on first success
	#'formv.validators.compound:VPipe',  # return if all succeed
	
	#'formv.validators.dates:VDate',  # earliest, latest, after_now, today_or_after, format
	#'formv.validators.dates:VTime',  #
	#'formv.validators.dates:VToDate',  # much more basic than VDate, strptime
	
	'formv.validators.encoders:VEncoded',  # crypt
	'formv.validators.encoders:VEncodedPair',  # a+b crypt (i.e. user+pass)
	
	'formv.validators.files:VUploadFile',  # tmpdir, mime_types, size, compress, resize, thumbnail, move_to, backup_to
	'formv.validators.files:VWatermarkImage',  # type, mode, text, layer, font, color, file, margin, opacity, angle
	'formv.validators.files:VImprintImage',  #
	'formv.validators.files:VTextToImage',  #
	
	#'formv.validators.geographic:VLatitude',  #
	#'formv.validators.geographic:VLongitude',  #
	#'formv.validators.geographic:VCountry',  #
	
	#'formv.validators.network:VIPAddress',  # inet_ntoa for ipv4 or ipv6 from the dns package
	#'formv.validators.network:VCIDR',  # ntoa, also using dns
	#'formv.validators.network:VMACAddress',  # basic algorithm; simpler is int(val.replace(':', ''), 16)
	
	#'formv.validators.numbers:VInteger',  #
	#'formv.validators.numbers:VFloat',  #
	#'formv.validators.numbers:VNumber',  #
	
	'formv.validators.schema:VSchema',  #
	
	'formv.validators.signers:VSignedString',  # b64 + hmac
	'formv.validators.signers:VSignedObject',  # as above, but pickled first
	
	#'formv.validators.strings:VString',  #
	#'formv.validators.strings:VRegex',  #
	#'formv.validators.strings:VText',  # regex ^[a-zA-Z_\-0-9]*$
	#'formv.validators.strings:VEmail',  # regex; permissive
	#'formv.validators.strings:VPassword',  # has stupid special character restriction option (i.e. [^a-zA-Z]{2,})
	#'formv.validators.strings:VURL',  # only http, https, ftp, uses urlparse; will optionally urlopen
	#'formv.validators.strings:VUserAgent',  # has default allowed/notallowed lists
]



class WebForm(VSchema):
	fields = {
		'first_name': VString(min_len=3, max_len=50),
		'last_name': VString(min_len=3, max_len=50),
		'postcode': VString(),
		'state': VString(),
		'country': VCountry(required=True, mode='by-name'),
		'email': VEmail(required=True),
		'password': VPassword(special_chars=3),
		'file_upload': VPipe(VUploadFile(mime_types=mime_types,
										 temp_dir='/tmp/formv/test/tmp',),
							 VWatermarkImage(type='image',
											 file=os.path.join(app_root, 'tests/watermarks/copyright.jpg'),
											 opacity=.04, angle=45),
							 VWatermarkImage(text='formv text watermark', angle=25,
											 color=(0,0,0,128), opacity=1),
							 VImprintImage(text='Note the image watermark in the background',
										   color=(0,128,128,255)),
							 VImprintImage(text=datetime.strftime(datetime.utcnow(),
																  'Uploaded on %Y/%m/%d - %H:%M:%S GMT'),
										   color=(255,128,128,255),
										   margin=(25,10)),
					   )
	}

	chains = {
		'coordinates': VCountryPostcode(country_field='country',     # extracts (latitude, longitude) pair
										postcode_field='postcode'),
		'password': VEncodedPair(required_field='password',          # encodes (password, email) pair
								 required_label='Password',
								 available_field='email'),
		'state': VState(country_field='country',                     # validates state against country
						state_field='state', mode='by-name'),
	}

form = WebForm(allow_missing_keys=True,
			   allow_extra_keys=True,
			   replace_empty_value=True,
			   empty_values={
				   # inject recovered file back into form if no new file has been uploaded
				   'file_upload': session.files.get('file_upload'),
			   })
return form.validate(request)

class WebForm(VSchema):
	""" form validator """

	fields = {
		'first_name': VString(min_len=3, max_len=50),
		'last_name': VString(min_len=3, max_len=50),
		'email': VEmail(required=True),
		'address':VString(),
		'postcode_start': VString(),
		'postcode_end': VString(),
		'state': VString(),
		'country': VCountry(required=True, mode='by-name'),
		'currency': VString(),
		'price': VFloat(),
		'units': VInteger(),
		'pay_method': VString(),
		'phone': VString(),
		'phone_type': VString(),
		'fax': VString(),
		'date': VPipe(VToDate(date_format='%d/%m/%Y'), VDate(today_or_after=False)),
		'missing_field': VString(),
		'username': VString(),
		'password': VPassword(special_chars=3),
		'file_pdf': VUploadFile(required=True,
								mime_types=mime_types,
								temp_dir='/tmp/formv/test/tmp',),
		'file_jpg': VPipe(VUploadFile(mime_types=mime_types,
									  temp_dir='/tmp/formv/test/tmp',),
						  VWatermarkImage(text='watermark'),
						  VImprintImage(text='imprint')),
		'file_csv': VUploadFile(mime_types=mime_types,
								temp_dir='/tmp/formv/test/tmp',),
		'file_empty': VUploadFile(mime_types=mime_types,
								  temp_dir='/tmp/formv/test/tmp',),
	}

	chains = {
		'contact': VAnyField(fields=('email', 'phone', 'fax'),
							 msg='Please provide some relevant, public contact details'),

		'state': VState(country_field='country',
						state_field='state', mode='by-name'),

		'currency': VCurrency(country_field='country',
							  currency_field='currency', mode='by-name'),

		'origin': VCountryPostcode(country_field='country',
								   postcode_field='postcode_start'),

		'destination': VCountryPostcode(country_field='country',
										postcode_field='postcode_end'),

		'phone_type': VPair(required_field='phone_type',
							required_label='Phone type',
							available_field='phone'),

		'pay_method': VPair(required_field='pay_method',
							required_label='Payment method',
							available_field='price'),

		'password': VEncodedPair(required_field='password',
								 required_label='VPassword',
								 available_field='username'),

		'z-geodist': VGeoDistance(origin_field='origin',
								  destination_field='destination'),
	}
