=====
cinje
=====

    © 2015 Alice Bevan-McGregor and contributors.

..

    https://github.com/marrow/cinje

..

    |latestversion| |downloads| |masterstatus| |mastercover| |issuecount|

1. What is cinje?
=================

cinje is a modern, elegant template engine constructed as a Python domain-specific-lanuage that integrates into your
applications as any other Python code would: by importing them.  Your templates are translated from their source into
clean, straightforward, and understandable Python source prior to the Python interpreter compiling it to bytecode.

1.1 Goals
---------

There is no shortage of template engines available in the Python ecosystem.  The following items help differentiate
cinje from the competition:

* Streaming is the primary goal.  The vast majority of template engines buffer the entire template during rendering,
  "yielding" the result once at the end.  This is disadvantageous for any page which involves large amounts of
  computation or the nessicary loading of resources such as fonts to correctly render.  With cinje you can "flush" the
  buffer at any point, allowing the browser to get the ``<head>`` section while the rest of the ``<body>`` is
  generating, as one example, leading to a more responsive experience for end-users.  Few engines (I could find none)
  support this directly.  Because the templates are of a streaming nature, template to code translation is also
  streaming.
* Many engines are implemented through custom parsing, lexing, and direct abstract syntax tree (AST) manipulation.
  These things are difficult to understand fully and quite an obstacle towards understanding for new users.  cinje
  avoids them by processing the template source as simple text in a clear, linear, single-pass fashion.
* The _template to Python source_ conversion code must be extensible to allow for the easy addition of new directives.
* Performance is less important than streaming functionality, but it should be at least "par" with similar engines
  such as ``mako`` or ``tenjin`` for complete rendering times.  Utilizing streaming functionality should not impose
  undue overhead.
* Utilize ``markupsafe`` if installed, but do not depend on it.  If not present cinje falls back on ``html.escape``.


2. Installation
===============

Installing ``cinje`` is easy, just execute the following in a terminal::

    pip install cinje

**Note:** We *strongly* recommend always using a container, virtualization, or sandboxing environment of some kind when
developing using Python; installing things system-wide is yucky (for a variety of reasons) nine times out of ten.  We prefer light-weight `virtualenv <https://virtualenv.pypa.io/en/latest/virtualenv.html>`_, others prefer solutions as robust as `Vagrant <http://www.vagrantup.com>`_.

If you add ``cinje`` to the ``install_requires`` argument of the call to ``setup()`` in your applicaiton's
``setup.py`` file, cinje will be automatically installed and made available when your own application or
library is installed.  We recommend using "less than" version numbers to ensure there are no unintentional
side-effects when updating.  Use ``cinje<1.2`` to get all bugfixes for the current release, and
``cinje<2.0`` to get bugfixes and feature updates while ensuring that large breaking changes are not installed.


2.1. Development Version
------------------------

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


3. Getting Started
==================

In order for imports of cinje template functions to correctly translate the source you must first import the ``cinje``
module in order to register the file encoding.  Once this has been done you can import functions from cinje modules
just like any other Python module.  Calling a cinje function is identical to calling a generator function, as all
cinje functions are generators.  This generator can be directly used as the ``body_iter`` value returned by WSGI
applications.


4. Basic Syntax
===============

If you have prior experience using template engines, the syntax should feel quite familiar.  Lines prefixed with a
colon (``:``) are "code".  Lines prefixed with a # are comments, excluding lines starting with a ``#{`` variable
replacement.  All other lines are treated as template text.  Template text is not allowed at the module level.

Code lines are processed by each of the different "block" and "inline" processor classes and runs of template text
are processed by the ``cinje.inline.text`` processor, with replacements processed by the ``cinje.util.chunk``
helper function.

4.1. Variable Replacement
-------------------------

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

The less-safe replacement does not escape HTML entities; you should sholud be careful where this is used.  For trusted
data, though, this form is somewhat more efficient.  In the generated code your expression will be wrapped in a call
to ``_bless()`` which defaults to the ``bless`` function imported from the ``cinje.helpers`` module.  If
``markupsafe`` is installed its ``Markup`` class will be used, otherwise the Python ``str`` function will be used.
The result is appended to the current buffer.

============================= ================================ ================================
cinje                         Python                           Result
============================= ================================ ================================
``#{27*42}``                  ``_bless(27*42)``                ``"1134"``
``${"<i>Hi.</i>"}``           ``_escape("<i>Hi.</i>")``        ``"<i>Hi.</i>"``
============================= ================================ ================================

HTML Attributes Replacement
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A frequent pattern in reusable templates is to provide some method to emit key/value pairs, with defaults, as HTML or
XML attributes.  To eliminate boilerplate cinje provides a replacement which handles this naturally.

Attributes which are literally ``True`` have no emitted value.  Attributes which are literally ``False`` or ``None``
are omitted.  A value can be provided, then defaults provided using the ``key=value`` keyword argument style; if the
key does not have a value in the initial argument, the default will be used.

=================================== ======================================= ================================
cinje                               Python                                  Result
=================================== ======================================= ================================
``&{dict(autocomplete=True)}``      ``_args(dict(autocomplete=True))``      ``" autocomplete"``
``&{dict(autocomplete=False)}``     ``_args(dict(autocomplete=False))``     ``""`` (empty)
``&{dict(name="Bob Dole")}``        ``_args(dict(name="Bob Dole"))``        ``' name="Bob Dole"'``
``&{somevar default=27}``           ``_args(somevar, default="hello")``     (depends on ``somevar``)
=================================== ======================================= ================================

A preceeding space will be emitted automatically if any values would be emitted.  The following would be correct:

	``<meta&{name=name, content=content}>``

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
a good idea to keep it short or provide it from a variable.




5. Version History
==================

Version 1.0
-----------

* Initial release.


6. License
==========

cinje has been released under the MIT Open Source license.

6.1. The MIT License
--------------------

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

.. |mastercover| image:: http://img.shields.io/coveralls/marrow/cinje/master.svg?style=flat
    :target: https://travis-ci.org/marrow/cinje
    :alt: Release Test Coverage

.. |developcover| image:: http://img.shields.io/coveralls/marrow/cinje/develop.svg?style=flat
    :target: https://travis-ci.org/marrow/cinje
    :alt: Development Test Coverage

.. |issuecount| image:: http://img.shields.io/github/issues/marrow/cinje.svg?style=flat
    :target: https://github.com/marrow/cinje/issues
    :alt: Github Issues

.. |cake| image:: http://img.shields.io/badge/cake-lie-1b87fb.svg?style=flat
