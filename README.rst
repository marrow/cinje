=====
cinje
=====

    © 2015-2019 Alice Bevan-McGregor and contributors.

..

    https://github.com/marrow/cinje

..

    |latestversion| |ghtag| |downloads| |masterstatus| |mastercover| |masterreq| |ghwatch| |ghstar|


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
      5. `JSON Object Replacement`_
   
   2. `Block Transformations`_
   
      1. `Module Scope`_
      2. `Function Declaration`_
      3. `Flow Control`_
   
   3. `Inline Transformations`_
   
      1. `Code`_
      2. `Comments`_
      3. `Flush`_
      4. `Text`_
   
   4. `Inheritance`_
  
5. `Version History`_
6. `License`_



What is cinje?
==============

Cinje is a modern, elegant template engine constructed as a Python domain specific language (DSL) that integrates into
your applications as any other Python code would: by importing them.  Your templates are transformed from their source
into clean, straightforward, and understandable Python source prior to the Python interpreter compiling it to bytecode.

What kind of name is cinje?!
----------------------------

It's a word from the constructed language `Lojban <http://www.lojban.org/>`_.  A combination of Hindi "śikana", English
"wrinkle", and Chinese "zhé".  It translates as "is a wrinkle/crease/fold [shape] in".  It's also a Hungarian noun
representing the posessive third-person singular form of "cin", meaning "tin".  The "c" makes a "sh" sound, the "j"
makes a "jy" sound almost like the "is" in "vision".  Correct use does not capitalize the name except at the beginning
of sentences.

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

* Virtually all perform low-level parsing, lexing, and Abstract Syntax Tree (AST) manipulation.  These things are
  difficult for developers new to the language to understand.  Additionally, many manually orchestrate Python's own
  parsing and compilation phases, and some even manually manage the bytecode cache.  This greatly increases the
  complexity of the engine itself.

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
side-effects when updating.  Use ``cinje<1.2`` to get all bugfixes for the current release, and
``cinje<2.0`` to get bugfixes and feature updates while ensuring that large breaking changes are not installed.

While cinje does not have any hard dependencies on any other package, it is **strongly** recommended that applications
using cinje also install the ``markupsafe`` package to provide more efficient string escaping and some additional
functionality such as object protocol support for markup generation.


Development Version
-------------------

    |developstatus| |developcover| |ghsince| |issuecount| |ghfork|

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

In order for imports of cinje template functions to correctly transform the source you must first ``import cinje``
in order to register the file encoding.  This may sound like magic, but it's not: it's just the Python unicode decoding
hook in the ``cinje.encoding`` module.  Once this has been done you can directly import functions from cinje modules.

Your cinje template files are Python modules like any other: they should have a ``.py`` filename extension and begin
with the the encoding declaration::

    # encoding: cinje

This tells Python to process the file using the ``cinje`` codec prior to interpreting the code.  Cinje itself assumes
the file is actually UTF-8 encoded.

Calling a cinje function is identical to calling a generator function, as all cinje template functions—those containing
text—are generators.  Normal template functions generate unicode fragments.  Wrapper template functions will at some
point generate a ``None`` value; you can iterate up to that point, and subsequently continue iterating after that
point using the ``cinje.util.interrupt`` iterator to iterate up to the first ``None``.

Primarily for testing small chunks of template template code in actual unit tests, two helpful functions are provided:

* ``cinje.fragment(string, name="anonymous", **context)`` Transform a template fragment into a callable function.
  
  Only one function may be declared, either manually, or automatically. If automatic defintition is chosen the
  resulting function takes no arguments.  Additional keyword arguments are passed through as global variables.

* ``cinje.flatten(input, file=None, encoding=None, errors='strict')`` Return a flattened representation of a cinje
  chunk stream.
  
  This has several modes of operation.  If no ``file`` argument is given, output will be returned as a string.
  The type of string will be determined by the presence of an ``encoding``; if one is given the returned value is a
  binary string, otherwise the native unicode representation.  If a ``file`` is present, chunks will be written
  iteratively through repeated calls to ``file.write()``, and the amount of data (characters or bytes) written
  returned.  The type of string written will be determined by ``encoding``, just as the return value is when not
  writing to a file-like object.  The ``errors`` argument is passed through when encoding.
  
  We can highly recommend using the various streaming IO containers available in the
  `io <https://docs.python.org/3/library/io.html>`_ module, though
  `tempfile <https://docs.python.org/3/library/tempfile.html>`_ classes are also quite useful.

* ``cinje.stream(input, encoding=None, errors='strict')`` Safely iterate a template generator, ignoring ``None``
  values and optionally stream encoding.  Used internally by ``cinje.flatten``, this allows for easy use of a template
  generator as a WSGI body.

You can always also transform arbitrary template source by passing it through ``.decode('cinje')``, which would return
the resulting transformed source code.


Basic Syntax
============

If you have prior experience using template engines, the syntax should feel quite familiar.  Lines prefixed with a
colon (``:``) are "code".  Lines prefixed with a hash mark (`#`) are comments.  All other lines are treated as
template text.  Template text is not allowed at the module level as it is not valid for a module to ``yield``.

Code lines are processed by each of the different "block" and "inline" processor classes and runs of template text
are processed by the ``cinje.inline.text`` processor, with replacements processed by the ``cinje.util.chunk``
helper function.

Text lines can have a "continuation" marker (``\``) on the end to denote that no newline should be emitted there.

We use a shell-like argument format for illustrating the syntax.


Variable Replacement
--------------------

There are several flavours of variable replacement available.  Within these use of curly braces is allowed only if
the braces are balanced.  Any of the helper functions mentioned can be overridden at the module or function level.

All variable replacement is a simple transformation of the source text into a function call wrapped version of the
source text.

HTML/XML Escaped Replacement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	``${<expr>}`` → ``_escape(<expr>)``

The default replacement operator is a Python expression surrounded by ``${`` and ``}``.  In the generated code your
expression will be wrapped in a call to ``_escape()`` which defaults to the ``escape`` function imported from the
``cinje.helpers`` module.  If ``markupsafe`` is installed its escaping function will be used, otherwise the Python-
standard ``html.escape`` function will be used.  Please see the
`MarkupSafe <https://pypi.python.org/pypi/MarkupSafe>`_ documentation for a full description of the additional
capabilities it offers.  The result is appended to the current buffer.

============================= ================================ ================================
cinje                         Python                           Result
============================= ================================ ================================
``${2+2}``                    ``_escape(2+2)``                 ``"4"``
``${"<i>Hi.</i>"}``           ``_escape("<i>Hi.</i>")``        ``"&lt;i&gt;Hi.&lt;/i&gt;"``
============================= ================================ ================================

Unescaped Replacement
~~~~~~~~~~~~~~~~~~~~~

	``#{<expr>}`` → ``_bless(<expr>)``

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

	``&{<argspec>}`` → ``_args(<argspec>)``

A frequent pattern in reusable templates is to provide some method to emit key/value pairs, with defaults, as HTML or
XML attributes.  To eliminate boilerplate cinje provides a replacement which handles this naturally and can help
users, especially users new to template engines, avoid certain common but hideous structures to conditionally add
attributes.

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

	``%{<expr> <argspec>}`` → ``_bless(<expr>).format(<argspec>)``

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

Any expression can be used for the "format string" expression, however for sanity's sake it's generally a good idea to
keep it as a short string literal or provide it from a variable.

**Note:** The format string is blessed, meaning it should not be sourced from user-supplied data, for security
reasons.  When MarkupSafe is *not* installed the replacements are passed through to Python-standard string formatting.
If, however, MarkupSafe *is* installed, then the replacements are escaped prior to formatting and additional
functionality is available to make your objects HTML-formatting aware.  (See the MarkupSafe documentation.)

JSON Object Replacement
~~~~~~~~~~~~~~~~~~~~~~~

	``@{<expr>}`` → ``_json(<expr>)``

It is sometimes useful to pass data through a template to JavaScript. This will emit the JSON-serialized version of
the expression result.


Block Transformations
---------------------

Block transformations typically denote some form of scope change or flow control, and must be terminated with an
"end" instruction.  Blocks not terminated by the end of the file will be automatically terminated, allowing trailing
terminators to be elided away and omitted from most templates.

Module Scope
~~~~~~~~~~~~

This is an automatic transformer triggered by the start of a source file.  It automatically adds a few imports to the
top of your file to import the required helpers from cinje.

By default the ``buffer`` flag is enabled in all modules.

Function Declaration
~~~~~~~~~~~~~~~~~~~~

	``: def <name-literal>[ <argspec>]`` → ``def <name-literal>([<argspec>][<scope-binding>]):``

Lines beginning with ``: def`` are used to declare functions within your template source::

	: def somefunction
		Hello world!
	: end

The above transforms to, roughly, the following Python source::

	def somefunction(*, _escape=_escape, _bless=_bless):
		_buffer = []
		_buffer.append(_bless("\tHello world!\n"))
		yield ''.join(_buffer)

You do not need the extraneous trailing colon to denote the end of the declaration, nor do you need to provide
parenthesis around the argument specification.  The optimization keyword-only arguments will be added automatically to
the argument specification you give on non-Pypy Python 3 versions.  It will gracefully handle integration into your
arglist even if your arglist already includes the keyword-only marker, or combinations of ``*args`` or ``**kw``.

You can specify flags to enable or disable within the context of a specific function using Python 3 function
annotations. These annotations will work for setting and unsetting flags across both Python 2 and Python 3 runtimes.

The most common use of per-function flags is to disable buffering, or enable whitespace stripping::

	: def anotherfunction -> !buffer strip
		This won't have a trailing newline, and will be immediately yielded.

The result of this would be::

	def anotherfunction(...):
		yield "This won't have a trailing newline, and will be immediately yielded."

Flags declared in this way will have their effect reversed automatically at the close of the function scope.

Flow Control
~~~~~~~~~~~~

	``: <statement>`` → ``<statement>:``

Cinje is fairly agnostic towards most Python flow control statements.  The ``cinje.block.generic`` transformer handles
most Python block scope syntax.  These include:

* **Conditionals** including ``if``, ``elif``, and ``else``.
* **Iterators** including ``while``, and ``for``, inlcuding the ``else`` block for ``for`` loops.
* **Context managers** via ``with``.
* **Exception handling** including ``try``, ``except``, ``finally``, and ``else``.

In all cases the only real transformation done is moving the colon from the beginning of the declared line to the end.

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


Inline Transformations
----------------------

Inline transformations are code lines that do not "start" a section that subsequently needs an "end".

Code
~~~~

Lines prefixed with a colon (``:``) that aren't matched by another transformation rule are treated as inline Python
code in the generated module.  Within these bits of code you do have access to the helpers and buffer, and so can
easily customize template rendering at will.

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
be un-flushed text in the buffer.  (Processing context marked with the "dirty" flag.)

Text
~~~~

Text covers every other line present in your template source.  Cinje efficiently gathers consecutive lines of template
text, collapses runs of static text into single strings, and splits the template text up to process replacements.

Template text is not permitted at the module scope as there can be no way to "yield" the buffer from there.  To save
on method calls, the following::

	<meta&{name=name, content=content}>

Is transformed, roughly, into the following single outer call and three nested calls::

	_buffer.extend((
		_bless('<meta'),
		_args(name=name, content=content),
		_bless('>')
	))

See the Variable Replacement section for details on the replacement options that are available and how they operate.

Pragma
~~~~~~

*New in Version 1.1*

The ``: pragma <flag>[ <flag>][...]`` directive allows you to enable or disable one or more processing flags. Usage is
straightforward; to add a flag to the current set of flags::

	: pragma flag

To subsequently remove a flag::

	: pragma !flag

Multiple flags may be whitespace separated and can mix addition and removal::

	: pragma flag !other_flag

No flag may contain whitespace. Built-in flags include:

* ``init``: The module scope has been prepared. Unsetting this is unwise.
* ``text``: Text fragments have been utilized within the current function, making this a template function.
* ``dirty``: It is known to the engine that the current buffer contains content which will need to be flushed.
* ``buffer``: Enabled by default, its presence tells cinje to use a buffer with explicit flushing. When removed,
  buffering is disabled and every fragment is flushed as it is encountered, and ``: use`` and ``: using`` behaviour
  is altered to ``yield from`` instead of adding the child template to the buffer.
  It is potentially very useful to disable this in the context of ``: use`` and ``: using`` to make child template
  ``: flush`` statements effective.
* ``using``: Indicates the ``_using_stack`` variable is available at this point in the translated code, i.e. to track
  nested ``: using`` statements.


Inheritance
-----------

Due to the streaming and "native Python code" natures of cinje, template inheritance is generally handled through
the standard definition of functions, and passing of those first-class objects around.  The most common case, where
one template "wraps" another, is handled through the ``: using`` and ``: yield`` directives.

An example "wrapper" template::

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

**Note:** Because the bare yield will produce a value of ``None``, wrapping functions like these are **not**
safe for use as a WSGI body iterable without wrapping in a generator to throw away ``None`` values.

The syntax for the ``using`` directive is ``: using <expr>[ <argspec>]``, thus to use this wrapper::

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

Lastly, there is a quick shortcut for consuming a template function and injecting its output into the current buffer::

	: use <expr>[ <argspec>]

And directly transforms to::

	_buffer.extend(<expr>(<argspec>))

Just like with ``using``, the result of the expression must be a callable generator function.


Version History
===============

Version 1.1.2
-------------

* *Fixed* `Python 3.7 exception use within generators. <https://github.com/marrow/cinje/issues/28>`_

* *Added* Genshi to the `benchmark comparison suite <https://github.com/marrow/cinje/wiki/Benchmarks#python-37>`_.

* *Fixed* minor docstring typo.

Version 1.1.1
-------------

* *Fixed* `incorrect double-decoding (#25) <https://github.com/marrow/cinje/issues/25>`_ of UTF-8 that was preventing
  use of templates containing non-ASCII text.

* *Fixed* incorrect variable reference in the built-in (`cinje.std.html`) list helper.

* *Added* Python 3.6 testing, pre-commit hooks, and Makefile-based automation.

* *Removed* Python 3.3 testing and support, `flake8` enforcement, and `tox` build/test automation.


Version 1.1
-----------

* *Enhanced Pypy support.* Pypy does not require optimizations which potentially obfuscate the resulting code.
  So we don't do them.

* *Fixed* incorrect `#{}` handling when it was the first non-whitepsace on a line. (#22)

* *Fixed* buffer iteration edge case if the first template text in a function is deeper than the function scope. (#21)

* *Python 3-style function annotations* can now be used to define function-wide "pragma" additions and removals, even
  on Python 2. (#8)

* *Pragma processing directives.* Processing flags can be set and unset during the translation process using
  `: pragma`.

* *Unbuffered mode.* Cinje can now operate in unbuffered mode. Each contiguous chunk is individually yielded. (#8)

* *Secret feature.* Have a cinje template? Want to more easily peek behind the curtain? (Sssh, it's a completely
  unsupported feature that even syntax colors if `pygments` is installed.) `python -m cinje source file.py`

Version 1.0
-----------

* Initial release.


License
=======

cinje has been released under the MIT Open Source license.

The MIT License
---------------

Copyright © 2015-2019 Alice Bevan-McGregor and contributors.

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


.. |ghwatch| image:: https://img.shields.io/github/watchers/marrow/cinje.svg?style=social&label=Watch
    :target: https://github.com/marrow/cinje/subscription
    :alt: Subscribe to project activity on Github.

.. |ghstar| image:: https://img.shields.io/github/stars/marrow/cinje.svg?style=social&label=Star
    :target: https://github.com/marrow/cinje/subscription
    :alt: Star this project on Github.

.. |ghfork| image:: https://img.shields.io/github/forks/marrow/cinje.svg?style=social&label=Fork
    :target: https://github.com/marrow/cinje/fork
    :alt: Fork this project on Github.

.. |masterstatus| image:: http://img.shields.io/travis/marrow/cinje/master.svg?style=flat
    :target: https://travis-ci.org/marrow/cinje/branches
    :alt: Release build status.

.. |mastercover| image:: http://img.shields.io/codecov/c/github/marrow/cinje/master.svg?style=flat
    :target: https://codecov.io/github/marrow/cinje?branch=master
    :alt: Release test coverage.

.. |masterreq| image:: https://img.shields.io/requires/github/marrow/cinje.svg
    :target: https://requires.io/github/marrow/cinje/requirements/?branch=master
    :alt: Status of release dependencies.

.. |developstatus| image:: http://img.shields.io/travis/marrow/cinje/develop.svg?style=flat
    :target: https://travis-ci.org/marrow/cinje/branches
    :alt: Development build status.

.. |developcover| image:: http://img.shields.io/codecov/c/github/marrow/cinje/develop.svg?style=flat
    :target: https://codecov.io/github/marrow/cinje?branch=develop
    :alt: Development test coverage.

.. |developreq| image:: https://img.shields.io/requires/github/marrow/cinje.svg
    :target: https://requires.io/github/marrow/cinje/requirements/?branch=develop
    :alt: Status of development dependencies.

.. |issuecount| image:: http://img.shields.io/github/issues-raw/marrow/cinje.svg?style=flat
    :target: https://github.com/marrow/cinje/issues
    :alt: Github Issues

.. |ghsince| image:: https://img.shields.io/github/commits-since/marrow/cinje/1.1.2.svg
    :target: https://github.com/marrow/cinje/commits/develop
    :alt: Changes since last release.

.. |ghtag| image:: https://img.shields.io/github/tag/marrow/cinje.svg
    :target: https://github.com/marrow/cinje/tree/1.1.2
    :alt: Latest Github tagged release.

.. |latestversion| image:: http://img.shields.io/pypi/v/cinje.svg?style=flat
    :target: https://pypi.python.org/pypi/cinje
    :alt: Latest released version.

.. |downloads| image:: http://img.shields.io/pypi/dw/cinje.svg?style=flat
    :target: https://pypi.python.org/pypi/cinje
    :alt: Downloads per week.

.. |cake| image:: http://img.shields.io/badge/cake-lie-1b87fb.svg?style=flat
