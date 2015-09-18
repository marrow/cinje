# encoding: cinje

: def _sample
	: using page "Hello world!"
		
		<p>This is, like, some content or something.</p>
		
	: end
: end


: def page title, *, metadata=[], styles=[], scripts=[], **attributes
: """A general HTML page."""

: if not attributes: attributes = {}

<!DOCTYPE html>
<html&{lang=attributes.pop('lang', 'en')}>
	<head>
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
	</head>
	
	<body&{attributes, role='document'}>
		: yield
		
		<script src="//cdn.jsdelivr.net/jquery/1.11.2/jquery.min.js"></script>
		
		<script>
			$(function(){
				$('a[data-toggle="tab"]').click(function(event) {
					var self = $(this);
					event.preventDefault();
					if ( self.hasClass('disabled') ) return;
					self.tab('show');
				});
				
				$('a[href^="#"]').click(function(event) {
					if ( !$(this.hash).length ) return;
					if ( $(this).data('toggle') == 'tab' ) return;
					event.preventDefault();
					$('html, body').animate({scrollTop: $(this.hash).offset().top}, 500);
				});
				
			});
		</script>
		
		: for href in scripts
		<script&{src=href}></script>
		: end
		
	</body>
</html>