# encoding: cinje

## This comment won't get included in the result.

: from collections import abc

: _list = list  # We override an important __builtin__ name in this module.


: def html **kwargs
	: """Standard HTML5 root tag."""
<!DOCTYPE html>
<html&{kwargs}>
	: yield
</html>
: end


: def meta name, content
	: """HTML5 metadata."""
	<meta name="${name}" content="${content}">
: end


: def page
	: """A general HTML page."""
	
	: using html
		
	<head>
	</head>
	<body>
		
		: yield
	
	</body>
	: end
: end


: def link href, **kwargs
	: """HTML5 hypertext reference."""
	<a href="${href}"&{kwargs}>
		: yield
	</a>
:end


: def div **kwargs
	: """Generic HTML5 block element."""
	<div&{kwargs}>
		: yield
	</div>
: end


: def span content, **kwargs
	: """Generic HTML5 inline element."""
	<span&{kwargs}>${content}</span>
: end


: def heading level=1, **kwargs
	: """Standard level-specific HTML5 heading."""
	<h${level}&{kwargs}>
		: yield
	</h${level}>
: end


: def abbr label, title, **kwargs
	: """HTML5 inline abbreviation."""
	<abbr title="${title}"&{kwargs}>${label}</abbr>
: end
 

: def list context, obj, kind='auto', flush=10, **attributes
	: """Generate an HTML5 list, defaulting to type auto-detection."""
	
	: if kind == 'auto'
		: if isinstance(obj, abc.Mapping)
			: kind = 'dl'
		: elif isinstance(obj, abc.Set)
			: kind = 'ul'
		: elif isinstance(obj, abc.Sequence)
			: kind = 'ol'
		: end
	: end
	
	<${kind}&{kwargs}>
		: if kind == 'dl'
			: for key in obj
				<dt>${key}</dt>
				<dd>${obj[key]}</dd>
			: end
		: else
			: for element in obj
				<li>${element}</li>
			: end
		: end
	</${kind}>
: end


: def page_sample content
	Some stuff prior to the page inclusion.
	
	: flush
	
	: using page
		
		:flush
		
		<p>This is some content:</p>
		
		#{content}
		
		:flush
		
	: end
	
	Some stuff after the page inclusion.
: end
