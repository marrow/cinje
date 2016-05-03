# encoding: cinje

# To use this module:
# : from cinje.std import html
# : using html.page ...

: from collections import Mapping, Set, Sequence, Iterator

: _list = list  # We override an important __builtin__ name in this module.


: def default_header title, metadata=[], styles=[], scripts=[]
	: """Prepare and generate the HTML <head> section."""
		
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		
	: for data in metadata
		: if isinstance(data, Iterator)
			: _buffer.extend(data)
		: elif isinstance(data, Mapping)
		<meta&{data}>
		: else
		<meta&{name=data[0], content=data[1]}>
		: end
	: end
		
		<title>${title}</title>
		
	: for href in styles
		<link&{href=href, rel="stylesheet"}>
	: end
	: for href in scripts
		<script&{src=href}></script>
	: end
: end


: def default_footer styles=[], scripts=[]
	: """Prepare and generate the HTML body postfix."""
	
	: for href in styles
		<link&{href=href, rel="stylesheet"}>
	: end
	: for href in scripts
		<script&{src=href}></script>
	: end
: end


: def page title, header=default_header, footer=default_footer, metadata=[], styles=[], scripts=[], **attributes
	: """A general HTML page."""
	
	: if attributes is None
		: attributes = {}
	: end
	
<!DOCTYPE html>
<html&{lang=attributes.pop('lang', 'en')}>
	<head>
		: if header
			: use header title, metadata=metadata, styles=styles, scripts=[]
		: end
	</head>
	
	<body&{attributes, role='document'}>
		: yield
		
		: if footer
			: use footer styles=[], scripts=scripts
		: end
	</body>
</html>
: end


# TODO: __url__ protocol support, take str() of object, url from __url__, 
: def link href, **kwargs
	: """HTML5 hypertext reference."""
<a href="${href}"&{kwargs}>\
		: yield
</a>\
:end


: def div **kwargs
	: """Generic HTML5 block element."""
<div&{kwargs}>
	: yield
</div>
: end


: def span content, **kwargs
	: """Generic HTML5 inline element."""
<span&{kwargs}>\
	: if isinstance(content, Iterator)
		: _buffer.extend(content)
	: else
${content}\
	: end
</span>\
: end


: def heading content, level=1, **kwargs
	: """Standard level-specific HTML5 heading."""
<h${level}&{kwargs}>\
	: if isinstance(content, Iterator)
		: _buffer.extend(content)
	: else
${content}\
	: end
</h${level}>
: end


: def abbr label, title, **kwargs
	: """HTML5 inline abbreviation."""
<abbr&{kwargs, title=title}>${label}</abbr>\
: end


: def list obj, kind='auto', **attributes
	: """Generate an HTML5 list, defaulting to type auto-detection."""
	
	: if kind == 'auto'
		: if isinstance(obj, Mapping)
			: kind = 'dl'
		: elif isinstance(obj, Set)
			: kind = 'ul'
		: elif isinstance(obj, Sequence)
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
