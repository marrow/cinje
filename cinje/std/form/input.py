# encoding: cinje

: from functools import partial
: from collections import namedtuple, Iterator, Mapping


: def _input identifier, label=None, help=None
<div class="form-group">
	: if callable(label)
		: use label class_='control-label', for_=identifier
	: elif label
	<label class="control-label" for="${identifier}">${label}</label>  
	: end
	
	: if help
	<div>
		: yield
		<span id="${identifier}-help" class="help-block">${help}</span>
	</div>
	: else
		: yield
	: end
</div>
: end


: def input name, label, help=None, **attributes
	: classes = list(attributes.pop('class_', ()))
	: classes.append('form-control')
	
	: if help
		: attributes['aria-describedby'] = attributes.get('id_', name) + '-help'
	: end
	
	: using _input label, help
		<input&{attributes name=name, id_=name, class_=classes}>
	: end
: end


: text = partial(input, type_='text')
: password = partial(input, type_='password')
: search = partial(input, type_='search')


: def area name, label, help=None, **attributes
	# TODO
: end
