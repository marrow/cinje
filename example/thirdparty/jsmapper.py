[
	'jsmapper.schema:Property',  # abc; name, types, default, to_dict_callback
	'jsmapper.schema:JSONSchema',  # schema, title, description, default, ref, enum, type, all_of, any_of, one_of, not_, format
	
	'jsmapper.types:PrimitiveType',  #
	'jsmapper.types:Array',  # items, additional_items, min_items, max_items, unique_items
	'jsmapper.types:Boolean',  #
	'jsmapper.types:Numeric',  # multiple_of, maximum, exclusive_maximum, minimum, exclusive_minimum
	'jsmapper.types:Integer',  #
	'jsmapper.types:Number',  #
	'jsmapper.types:Null',  #
	'jsmapper.types:Object',  # max_properties, min_properties, required, additional_properties, properties, pattern_properties, dependencies
	'jsmapper.types:String',  # max_length, min_length, pattern
]