=====
cinje
=====

    © 2015 Alice Bevan-McGregor and contributors.

..

    https://github.com/marrow/cinje

..

    |latestversion| |downloads| |masterstatus| |mastercover| |issuecount|



Contents
========

1. `What is cinje?`_

   1. `What kind of name is cinje?!`_
   2. `Rationale and Goals`_

2. `Installation`_

   1. `Development Version`_

3. `Getting Started`_
4. `Basic Syntax`_

   1. `Variable Replacement`_
   
      1. `HTML/XML Escaped Replacement`_
      2. `Unescaped Replacement`_
      3. `HTML Attributes Replacement`_
      4. `Formatted Replacement`_
   
   2. `Block Transformations`_
   
      1. `Module Scope`_
      2. `Function Declaration`_
      3. `Conditional Flow`_
      4. `Iteration`_
      5. `Inheritance`_

   3. `Inline Transformations`_
   
      1. `Code`_
      2. `Comments`_
      3. `Flush`_
      4. `Text`_

5. `Version History`_
6. `License`_



What is cinje?
==============

cinje is a modern, elegant template engine constructed as a Python domain specific language (DSL) that integrates into
your applications as any other Python code would: by importing them.  Your templates are translated from their source
into clean, straightforward, and understandable Python source prior to the Python interpreter compiling it to bytecode.

What kind of name is cinje?!
----------------------------

It's a word from the constructed language `Lojban <http://www.lojban.org/>`_.  A combination of Hindi "śikana", English
"wrinkle", and Chinese "zhé".  It translates as "is a wrinkle/crease/fold [shape] in".  It's also a Hungarian noun
representing the posessive third-person singular form of "cin", meaning "tin".  The "c" makes a "sh" sound, the "j"
makes a "jy" sound almost like the "is" in "vision".  Correct use does not capitalize the name.

Rationale and Goals
-------------------

There is no shortage of template engines available in the Python ecosystem.  The following items help differentiate
cinje from the competition:

* There are few to no high-performance template engines which support:

  - Mid-stream flushing for delivery of partial content as it generates.  The vast majority of engines buffer the
    entire template during rendering, returning the result once at the end.  This is disadvantageous for any content
    which involves large amounts of computation, and prevents browsers from eagerly loading external static assets.  By
    comparison, cinje supports a ``: flush`` command to yield the buffer generated so far.
  
  - Direct use as a WSGI iterable body.  In cinje, template functions are generators which can be used directly as a
    WSGI body.  With no explicit ``: flush`` commands behaviour matches other engines: the buffer will be yielded once,
    at the end.

* Virtually all require boilerplate to "load" then "render" the template, such as instantiating a ``Template`` class
  and calling a ``render`` method, which is silly and a waste of repeated developer effort.  Alternatively, complex
  framework-specific adapters can be used for boilerplate-free engine use, but this solution is sub-optimal.  Since
  almost all generate Python code in the end, why not treat the templates as Python modules to start with and let the
  language, which already has all of this machinery, do what it was designed to do?  This is what cinje does.

* Virtually all perform low-level parsing, lexing, and AST manipulation.  These things are difficult for developers
  new to the language to understand.  Additionally, many manually orchestrate Python's own parsing and compilation
  phases, and some even manually manage the bytecode cache.  This greatly increases the complexity of the engine itself.

* Only a small minority of engines offer extensible syntax which allows for the creation of new directives.

* Performance is less important than streaming functionality, but it should be at least "par" with similar engines
  such as ``mako`` or ``tenjin`` for complete rendering times.  Utilizing streaming functionality should not impose
  undue overhead.  The capability to stream and be reasonably fast should neither obfuscate the template engine code
  nor obfuscate the generated template code.

Installation
============

Installing ``cinje`` is easy, just execute the following in a terminal::

    pip install cinje

**Note:** We *strongly* recommend always using a container, virtualization, or sandboxing environment of some kind when
developing using Python; installing things system-wide is yucky (for a variety of reasons) nine times out of ten.  We
prefer light-weight `virtualenv <https://virtualenv.pypa.io/en/latest/virtualenv.html>`_, others prefer solutions as
robust as `Vagrant <http://www.vagrantup.com>`_.

If you add ``cinje`` to the ``install_requires`` argument of the call to ``setup()`` in your application's
``setup.py`` file, cinje will be automatically installed and made available when your own application or
library is installed.  We recommend using "less than" version numbers to ensure there are no unintentional
side-effects when updating.  Use ``cinje<1.1`` to get all bugfixes for the current release, and
``cinje<2.0`` to get bugfixes and feature updates while ensuring that large breaking changes are not installed.


Development Version
-------------------

    |developstatus| |developcover|

Development takes place on `GitHub <https://github.com/>`_ in the
`cinje <https://github.com/marrow/cinje/>`_ project.  Issue tracking, documentation, and downloads
are provided there.

Installing the current development version requires `Git <http://git-scm.com/>`_, a distributed source code management
system.  If you have Git you can run the following to download and *link* the development version into your Python
runtime::

    git clone https://github.com/marrow/cinje.git
    (cd cinje; python setup.py develop)

You can then upgrade to the latest version at any time::

    (cd cinje; git pull; python setup.py develop)

If you would like to make changes and contribute them back to the project, fork the GitHub project, make your changes,
and submit a pull request.  This process is beyond the scope of this documentation; for more information see
`GitHub's documentation <http://help.github.com/>`_.


Getting Started
===============

In order for imports of cinje template functions to correctly translate the source you must first ``import cinje``
in order to register the file encoding.  This may sound like magic, but it's not: it's just the Python unicode decoding
hook in the ``cinje.encoding`` module.  Once this has been done you can directly import functions from cinje modules.

Your cinje template files are Python modules like any other: they should have a ``.py`` filename extension and begin
with the the encoding declaration::

    # encoding: cinje

This tells Python to process the file using the ``cinje`` codec prior to interpreting the code.  cinje itself assumes
the file is actually UTF-8 encoded.

Calling a cinje function is identical to calling a generator function, as all cinje template functions—those containing
text—are generators.  Normal template functions generate unicode fragments.  Wrapper template functions will at some
point generate a ``None`` value; you can iterate up to that point, and subsequently continue iterating after that
point using the ``cinje.util.interrupt`` iterator to iterate up to the first ``None``.


Basic Syntax
============

If you have prior experience using template engines, the syntax should feel quite familiar.  Lines prefixed with a
colon (``:``) are "code".  Lines prefixed with a # are comments, excluding lines starting with a ``#{`` variable
replacement.  All other lines are treated as template text.  Template text is not allowed at the module level.

Code lines are processed by each of the different "block" and "inline" processor classes and runs of template text
are processed by the ``cinje.inline.text`` processor, with replacements processed by the ``cinje.util.chunk``
helper function.

Text lines can have a "continuation" marker (``\``) on the end to denote that no newline should be emitted there.

Variable Replacement
--------------------

There are several flavours of variable replacement available.  Within these use of curly braces is allowed only if
the braces are balanced.  Any of the helper functions mentioned can be overridden at the module or function level.

HTML/XML Escaped Replacement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default replacement operator is a Python expression surrounded by ``${`` and ``}``.  In the generated code your
expression will be wrapped in a call to ``_escape()`` which defaults to the ``escape`` function imported from the
``cinje.helpers`` module.  If ``markupsafe`` is installed its escaping function will be used, otherwise the Python-
standard ``html.escape`` function will be used.  The result is appended to the current buffer.

============================= ================================ ================================
cinje                         Python                           Result
============================= ================================ ================================
``${2+2}``                    ``_escape(2+2)``                 ``"4"``
``${"<i>Hi.</i>"}``           ``_escape("<i>Hi.</i>")``        ``"&lt;i&gt;Hi.&lt;/i&gt;"``
============================= ================================ ================================

Unescaped Replacement
~~~~~~~~~~~~~~~~~~~~~

The less-safe replacement does not escape HTML entities; you should be careful where this is used.  For trusted
data, though, this form is somewhat more efficient.  In the generated code your expression will be wrapped in a call
to ``_bless()`` which defaults to the ``bless`` function imported from the ``cinje.helpers`` module.  If
``markupsafe`` is installed its ``Markup`` class will be used, otherwise the Python ``str`` function will be used.
The result is appended to the current buffer.

============================= ================================ ================================
cinje                         Python                           Result
============================= ================================ ================================
``#{27*42}``                  ``_bless(27*42)``                ``"1134"``
``#{"<i>Hi.</i>"}``           ``_bless("<i>Hi.</i>")``         ``"<i>Hi.</i>"``
============================= ================================ ================================

HTML Attributes Replacement
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A frequent pattern in reusable templates is to provide some method to emit key/value pairs, with defaults, as HTML or
XML attributes.  To eliminate boilerplate cinje provides a replacement which handles this naturally.

Attributes which are literally ``True`` have no emitted value.  Attributes which are literally ``False`` or ``None``
are omitted.  Non-string iterables are treated as a space-separated set of strings, for example, for use as a set of
CSS classes.  Trailing underscores are removed, to allow for use of Python-reserved words.  Single underscores
(``_``) within the key are replaced with hyphens.  Double underscores (``__``) within a key are replaced with colons.

A value can be provided, then defaults provided using the ``key=value`` keyword argument style; if the key does not
have a value in the initial argument, the default will be used.

=================================== ======================================= ================================
cinje                               Python                                  Result
=================================== ======================================= ================================
``&{autocomplete=True}``            ``_args(autocomplete=True)``            ``" autocomplete"``
``&{autocomplete=False}``           ``_args(autocomplete=False)``           ``""`` (empty)
``&{data_key="value"}``             ``_args(data_key="value")``             ``' data-key="value"'``
``&{xmlns__foo="bob"}``             ``_args(xmlns__foo="bob")``             ``' xmlns:bob="foo"'``
``&{name="Bob Dole"}``              ``_args(name="Bob Dole")``              ``' name="Bob Dole"'``
``&{somevar, default=27}``          ``_args(somevar, default="hello")``     (depends on ``somevar``)
=================================== ======================================= ================================

A preceeding space will be emitted automatically if any values would be emitted.  The following would be correct::

	<meta&{name=name, content=content}>

Formatted Replacement
~~~~~~~~~~~~~~~~~~~~~

Modern string formatting in Python utilizes the ``str.format`` string formatting system.  To facilitate replacements
using the advanced formatting features available in ``markupsafe`` while removing common boilerplate the "formatted
replacement" is made available.  Your source expression undergoes some mild reformatting, similar to that applied to
function declarations, seen later.

=================================== ===============================================
cinje                               Python
=================================== ===============================================
``%{somevar 42, num=27}``           ``_bless(somevar).format(42, num=27)``
``%{"Lif: {}  {num}" 42, num=27}``  ``_bless("Lif: {}  {num}").format(42, num=27)``
=================================== ===============================================

Any expression can be used for the "format string" part of the replacement, however for sanity's sake it's generally
a good idea to keep it as a short string literal or provide it from a variable.

Block Transformations
---------------------

Block transformations typically denote some form of scope change or flow control, and must be terminated with an
"end" instruction.  Blocks not terminated by the end of the file will be automatically terminated, allowing trailing
terminators to be elided away and omitted from most templates.

Module Scope
~~~~~~~~~~~~

This is an automatic transformer triggered by the start of a source file.  It automatically adds a few imports to the
top of your file to import the required helpers from cinje.


Function Declaration
~~~~~~~~~~~~~~~~~~~~

Lines beginning with ``: def`` are used to declare functions within your template source::

	: def somefunction
		Hello world!
	: end

The above translates to, roughly, the following Python source::

	def somefunction(*, _escape=_escape, _bless=_bless):
		_buffer = []
		__w = _buffer.extend
		__w((_bless("\tHello world!\n"), ))
		yield ''.join(_buffer)

You do not need the extraneous trailing colon to denote the end of the declaration, nor do you need to provide
parenthesis around the argument specification.  The optimization keyword-only arguments will be added automatically to
the argument specification you give on Python 3.  It will gracefully handle integration into your arglist even if your
arglist already includes the keyword-only marker, or combinations of ``*args`` or ``**kw``.  For example::

	: def hello name
		Hello ${name}!
	: end

Would translate to::

	def hello(name, *, _escape=_escape, _bless=_bless):
		_buffer = []
		__w = _buffer.extend
		__w((_bless("\tHello "), _escape(name), _bless("!\n")))
		yield ''.join(_buffer)

If your template file only contains one function, i.e. it's a full page template, you can omit the final ``: end``.

Conditional Flow
~~~~~~~~~~~~~~~~

Conditional template generation is integral to any engine that could call itself complete.  To facilitate this cinje
performs very light translation.  Similar to function declaration, trailing colons are unneeded::

	: if name
		Hello ${name}!
	: elif name == "Bob Dole"
		Mehp, ${name}!
	: else
		Hello world!
	: end

The translation is straightforward::

	if name:
		# …
	elif name == "Bob Dole":
		# …
	else:
		…


Iteration
~~~~~~~~~

Nearly identical to conditional flow, iteration is directly supported::

	: for name in names
		Hello ${name}!
	: end

Translates to::

	for name in names:
		# …

A helper is provided called ``iterate`` which acts similarly to ``enumerate`` but can provide additional details.
It's a generator that yields ``namedtuple`` values in the form ``(first, last, index, total, value)``.  If the current
loop iteration represents the first iteration, ``first`` will be True.  Similarly—and even for generators where a
total number of values being iterated could not be calculated beforehand—on the final iteration ``last`` will be True.
The ``index`` value is an atomic counter provided by ``enumerate``, and ``total`` will be the total number of elements
being iterated if the object being iterated supports length determination.  You can loop over its results directly::

	: for item in iterate(iterable)
		: if item.first
			…
		: end
	: end

You can also unpack them::

	: for first, last, index, total, value in iterate(iterable)
		…
	: end

If you wish to unpack the values being iterated, you can wrap the additional unpacking in a tuple::

	: for first, last, i, total, (foo, bar, baz) in iterate(iterable)
		…
	: end


Inheritance
~~~~~~~~~~~

Due to the streaming and "native Python code" natures of cinje, template inheritance is generally handled through
the standard definition of functions, and passing of those first-class objects around.  The most common case, where
one template "wraps" another, is handled through the ``: using`` and ``: yield`` directives.

An example "parent" template::

	: def page **properties
	<html>
		<body&{properties}>
			: yield
		</body>
	</html>
	: end

When called, functions that include a bare yield (and only one is allowed per function) will flush their buffers
automatically prior to the yield, then flush automatically at the end of the function, just like any other.  This has
the effect of extending the wrapped template's buffer by, at a minimum, two elements (prefix and suffix), though
additional ``: flush`` statements within the wrapper are allowed.

**Important note:** Because the bare yield will produce a value of ``None``, wrapping functions like these are **not**
safe for direct use as a WSGI body iterable.

Subsequently, to use this wrapper::

	: using page
		<p>Hello world!</p>
	: end

Execution of this would produce the following HTML::

	<html>
		<body>
			<p>Hello world!</p>
		</body>
	</html>

Because wrapping templates are just template functions like any other, you can pass arguments to them.  In the above
example we're using arbitrary keyword arguments as an "HTML attribute" replacement.  The following::

	: using page class_="hero"
	: end

Would produce the following::

	<html>
		<body class="hero">
		</body>
	</html>

Similar to having a single-function file, if your whole template is wrapped you can omit the trailing ``: end`` as one
will be added for you automatically if it is missing.

Inline Transformations
----------------------

Inline transformations are code lines that do not "start" a section that subsequently needs an "end".

Code
~~~~

Lines prefixed with ``:`` that aren't matched by another transformation rule are treated as inline Python code in the
generated module.  Within these bits of code you do have access to the helpers and buffer, and so can easily customize
template rendering at runtime.

The only lines acceptable at the module scope are code and comments.

Comments
~~~~~~~~

Basic comments are preserved in the final Python source.  Any line starting with the Python-standard line comment
prefix, a ``#`` hash mark or "pound" symbol, that doesn't match another rule, will be preserved as a comment.  If the
line is instead prefixed with a double hash mark ``##`` the comment will be stripped and *not* included in the final
Python module.

Flush
~~~~~

The ``: flush`` statement triggers cinje to emit the Python code needed to yield the current contents of the template
buffer and clear it.  The result, in Python, is roughly analogous to::

	yield ''.join(_buffer)
	_buffer.clear()

A flush is automatically triggered when falling off the bottom of a template function if it is known that there will
be un-flushed text in the buffer.

Text
~~~~

Text covers every other line present in your template source.  cinje efficiently gathers consecutive lines of template
text, collapses runs of static text into single strings, and splits the template text up to process replacements.

Template text is not permitted at the module scope as there can be no way to "yield" the buffer from there.  To save
on method calls, the following::

	<meta&{name=name, content=content}>

Is translated, roughly, into the following single outer call and three nested calls::

	__w((
		_bless('<meta'),
		_args(name=name, content=content),
		_bless('>')
	))

See the Variable Replacement section for details on the replacement options that are available and how they operate.


Version History
===============

Version 1.0
-----------

* Initial release.


License
=======

cinje has been released under the MIT Open Source license.

The MIT License
---------------

Copyright © 2015 Alice Bevan-McGregor and contributors.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


.. |masterstatus| image:: http://img.shields.io/travis/marrow/cinje/master.svg?style=flat
    :target: https://travis-ci.org/marrow/cinje
    :alt: Release Build Status

.. |developstatus| image:: http://img.shields.io/travis/marrow/cinje/develop.svg?style=flat
    :target: https://travis-ci.org/marrow/cinje
    :alt: Development Build Status

.. |latestversion| image:: http://img.shields.io/pypi/v/cinje.svg?style=flat
    :target: https://pypi.python.org/pypi/cinje
    :alt: Latest Version

.. |downloads| image:: http://img.shields.io/pypi/dw/cinje.svg?style=flat
    :target: https://pypi.python.org/pypi/cinje
    :alt: Downloads per Week

.. |mastercover| image:: http://img.shields.io/codecov/c/github/marrow/cinje/master.svg?style=flat
    :target: https://travis-ci.org/marrow/cinje
    :alt: Release Test Coverage

.. |developcover| image:: http://img.shields.io/codecov/c/github/marrow/cinje/develop.svg?style=flat
    :target: https://travis-ci.org/marrow/cinje
    :alt: Development Test Coverage

.. |issuecount| image:: http://img.shields.io/github/issues/marrow/cinje.svg?style=flat
    :target: https://github.com/marrow/cinje/issues
    :alt: Github Issues

.. |cake| image:: http://img.shields.io/badge/cake-lie-1b87fb.svg?style=flat
