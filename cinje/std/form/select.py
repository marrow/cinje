# encoding: cinje

: from operator import attrgetter as attr
: from itertools import groupby
: from collections import namedtuple, Iterator, Mapping


: group = namedtuple('group', ('label', 'disabled'))
: option = namedtuple('option', ('value', 'label', 'disabled', 'group'))


: def options choices
	: if not choices
		: return
	: end
	
	: if callable(choices)
		: choices = choices()
	: end
	
	: if isinstance(choices, Mapping)
		: for group in choices
			: for choice in choices[group]
				: if isinstance(choice, option)
					: yield choice
				: elif isinstance(choice, tuple)
					: yield option(choice[0], choice[1], False, group)  # (value, label)
				: elif isinstance(choice, Mapping)
					: args = dict(label=choice.get('value'), disabled=False, group=group)
					: args.update(choice)
					: yield option(**args)
				: else
					: yield option(choice, choice, False, group)
				: end
			: end
		: end
	: else
		: for choice in choices
			: if isinstance(choice, option)
				: yield choice
			: elif isinstance(choice, tuple)
				: if len(choice) == 3  # (group, value, label)
					: yield option(choice[1], choice[2], False, choice[0])
				: else
					: yield option(choice[0], choice[1], False, None)  # (value, label)
				: end
			: elif isinstance(choice, Mapping)
				: args = dict(label=choice.get('value'), disabled=False, group=None)
				: args.update(choice)
				: yield option(**args)
			: else
				: yield option(choice, choice, False, group)
			: end
		: end
	: end
: end


: def _basic_comparator selected, value
	: if selected is None
		: return value is None
	: end
	
	: return value == selected
: end


: def _iterator_comparator iterator, value
	: return value in iterator
: end


: def select name=None, choices=None, selected=None, **attributes
	: """A factory for HTML <select> elements."""
	
	: if isinstance(selected, (tuple, list, Iterator))
		: comparator = _iterator_comparator
	: else
		: comparator = _basic_comparator
	: end

<select&{attributes, name=name}>
	: for group, options in groupby(options(choices), attr('group'))
		: if group
	<optgroup&{label=group.label, disabled=group.disabled}>
		: end
		
		: for option in options
	<option&{value=option.value, disabled=option.disabled, selected=comparator(selected, option.value)}>${option.label}</option>
		: end
		
		: if group
	</optgroup>
		: end
	: end
</select>
