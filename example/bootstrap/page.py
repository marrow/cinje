# encoding: cinje

: def _sample
	: """A demonstration of how to utilize the page wrapper."""
	
	: def custom_footer *, styles=[], scripts=[]
		: """No jQuery by default on this page, for some reason."""
		
		: for href in scripts
		<script&{src=href}></script>
		: end
	: end
	
	: using page "Hello world!", footer=custom_footer
		
		<p>This is, like, some content or something.</p>
		
	: end
: end


: def _bench identifier
	: """A benchmark helper to ensure the whole template isn't interned."""
	
	: identifier = str(identifier)
	
	: using page "Hello " + identifier
		<p>Page ${identifier} reporting for duty!</p>
	: end
: end


: def header title, *, metadata=[], styles=[], scripts=[]
: """Prepare and generate the HTML <head> section."""
		
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		
		: for name, value in metadata
		<meta&{name=name, content=value}>
		: end
		
		<title>${title}</title>
		
		: for href in styles
		<link&{href=href, rel="stylesheet"}>
		: end
		
		<!--[if lt IE 9 ]>
		<script src="//cdn.jsdelivr.net/html5shiv/3.7.2/html5shiv-printshiv.min.js"></script>
		<script src="//cdn.jsdelivr.net/respond/1.4.2/respond.min.js"></script>
		<![endif]-->
: end


: def footer *, styles=[], scripts=[]
: """Prepare and generate the HTML body postfix."""
		
		<script src="//cdn.jsdelivr.net/jquery/1.11.2/jquery.min.js"></script>
		
		: for href in scripts
		<script&{src=href}></script>
		: end
: end


: def page title, *, header=None, footer=None, metadata=[], styles=[], scripts=[], **attributes
: """A general HTML page."""

: if attributes is None: attributes = {}

<!DOCTYPE html>
<html&{lang=attributes.pop('lang', 'en')}>
	<head>
		: __w(header(title, metadata=metadata, styles=styles, scripts=scripts) if header else ())
	</head>
	
	<body&{attributes, role='document'}>
		: yield
		
		: __w(footer(styles=styles, scripts=scripts) if footer else ())
	</body>
</html>