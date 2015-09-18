=============
Marrow Schema
=============

    © 2013-2015 Alice Bevan-McGregor and contributors.

..

    https://github.com/marrow/schema

..

    |latestversion| |downloads| |masterstatus| |mastercover| |issuecount|

1. What is Marrow Schema?
=========================

Marrow Schema is a tiny and fully tested, Python 2.6+ and 3.2+ compatible declarative syntax toolkit.  This basically
means you use high-level objects to define other high-level object data structures.  Simplified: you'll never have
to write a class constructor that only assigns instance variables again.

Examples of use include:

* Attribute-access dictionaries with predefined "slots".

* The object mapper aspect of an ORM or ODM for database access.

* Declarative schema-driven serialization systems.

* `Marrow Interface <https://github.com/marrow/marrow.interface>`_, declarative schema validation for arbitrary Python
  objects similar in purpose to ``zope.interface`` or Python's own abstract base classes.

* `Marrow Widgets <https://github.com/marrow/marrow.widgets>`_ are defined declaratively allowing for far more flexible
  and cooperative subclassing.

* Powerful data validation and transformation using the included frameworks.


1.1 Goals
---------

Marrow Schema was created with the goal of extracting a component common to nearly every database ORM, ODM, widget
system, form validation library, structured serialzation format, or other schema-based tool into a common shared
library to benefit all.  While some of the basic principles (data descriptors, etc.) are relatively simple, few
implementations are truly complete.  Often you would lose access to standard Python idioms such as the use of
positional arguments with class constructors or Pythonic exceptions.

With a proven generic implementation we discovered quickly that the possibilities weren't limited to the typical uses.
One commercial project that uses Marrow Schema does so to define generic CRUD *controllers* declaratively, greatly
reducing development time and encouraging WORM (write-once, read-many) best practice.

Marrow Schema additionally aims to have a very narrow scope and to "eat its own dog food", using a declarative syntax
to define the declarative syntax. This is in stark contrast to alternatives (such as
`scheme <https://github.com/siq/scheme/>`_) which utilize multiple metaclasses and a hodge-podge of magical attributes
internally.  Or `guts <https://github.com/emolch/guts/>`_, which is heavily tied to its XML and YAML data processing
capabilities.  Neither of these currently support positional instantiation, and both can be implemented as a
light-weight superset of Marrow Schema.


2. Installation
===============

Installing ``marrow.schema`` is easy, just execute the following in a terminal::

    pip install marrow.schema

**Note:** We *strongly* recommend always using a container, virtualization, or sandboxing environment of some kind when
developing using Python; installing things system-wide is yucky (for a variety of reasons) nine times out of ten.  We prefer light-weight `virtualenv <https://virtualenv.pypa.io/en/latest/virtualenv.html>`_, others prefer solutions as robust as `Vagrant <http://www.vagrantup.com>`_.

If you add ``marrow.schema`` to the ``install_requires`` argument of the call to ``setup()`` in your applicaiton's
``setup.py`` file, Marrow Schema will be automatically installed and made available when your own application or
library is installed.  We recommend using "less than" version numbers to ensure there are no unintentional
side-effects when updating.  Use ``marrow.schema<1.2`` to get all bugfixes for the current release, and
``marrow.schema<2.0`` to get bugfixes and feature updates while ensuring that large breaking changes are not installed.


2.1. Development Version
------------------------

    |developstatus| |developcover|

Development takes place on `GitHub <https://github.com/>`_ in the
`marrow/schema <https://github.com/marrow/schema/>`_ project.  Issue tracking, documentation, and downloads
are provided there.

Installing the current development version requires `Git <http://git-scm.com/>`_, a distributed source code management
system.  If you have Git you can run the following to download and *link* the development version into your Python
runtime::

    git clone https://github.com/marrow/schema.git
    (cd schema; python setup.py develop)

You can then upgrade to the latest version at any time::

    (cd schema; git pull; python setup.py develop)

If you would like to make changes and contribute them back to the project, fork the GitHub project, make your changes,
and submit a pull request.  This process is beyond the scope of this documentation; for more information see
`GitHub's documentation <http://help.github.com/>`_.


3. Basic Concepts
=================

3.1. Element
------------

Instantiation order tracking and attribute naming / collection base class.

To use, construct subclasses of the ``Element`` class whose attributes are themselves instances of ``Element``
subclasses.  Five attributes on your subclass have magical properties:

* ``inst.__sequence__`` — 
  An atomically incrementing (for the life of the process) counter used to preserve order.  Each instance of an
  ``Element`` subclass is given a new sequence number automatically.
  
* ``inst.__name__`` — 
  ``Element`` subclasses automatically associate attributes that are ``Element`` subclass instances with the name of
  the attribute they were assigned to.
  
* ``cls.__attributes__`` — 
  An ordered dictionary of all ``Element`` subclass instances assigned as attributes to your class. Class inheritance
  of this attribute is handled differently: it is a combination of the ``__attributes__`` of all parent classes.
  **Note:** This is only calculated at class construction time; this makes it efficient to consult frequently.
  
* ``cls.__attributed__`` — 
  Called after class construction to allow you to easily perform additional work, post-annotation.  Should be a
  classmethod for full effect.
  
* ``cls.__fixup__`` — 
  If an instance of your ``Element`` subclass is assigned as a property to an ``Element`` subclass, this method of your
  class will be called to notify you and allow you to make additional adjustments to the class using your subclass.
  Should be a classmethod.

Generally you will want to use one of the helper classes provided (``Container``, ``Attribute``, etc.) however this can
be useful if you only require extremely light-weight attribute features on custom objects.

3.2. Container
--------------

The underlying machinery for handling class instantiation for schema elements whose primary purpose is containing other
schema elements, i.e. ``Document``, ``Record``, ``CompoundWidget``, etc.

Association of declarative attribute names (at class construction time) is handled by the ``Element`` metaclass.

Processes arguments and assigns values to instance attributes at class instantiation time, basically defining
``__init__`` so you don't have to.  You could extend this to support validation during instantiation, or to process
additional programmatic arguments, as examples, and benefit from not having to repeat the same leg-work each time.

``Container`` subclasses have one additional magical property:

* ``inst.__data__`` — 
  Primary instance data storage for all ``DataAttribute`` instances.  Equivalent to ``_data`` from MongoEngine.

Most of the data storage requirements of Marrow Schema-derived objects comes from this dictionary.  Additionally,
Marrow Schema-derived objects tend to move data from the instance ``__dict__`` to this ``__data__`` dictionary, having
an unfortunate side-effect on the class-based performance optimizations of Pypy.  We hope to resolve this in the future
through optional annotations for that interpreter.

3.3. DataAttribute
------------------

Descriptor protocol support for ``Element`` subclasses.

The base attribute class which implements the descriptor protocol, pulling the instance value of the attribute from
the containing object's ``__data__`` dictionary.  If an attempt is made to read an attribute that does not have a
corresponding value in the data dictionary an ``AttributeError`` will be raised.

3.4. Attribute
--------------

Re-naming, default value, and container support for data attributes.

All "data" is stored in the container's ``__data__`` dictionary.  The key defaults to the ``Attribute`` instance name
and can be overridden, unlike ``DataAttribute``, by passing a name as the first positional parameter, or as the
``name`` keyword argument.

May contain nested ``Element`` instances to define properties for your ``Attribute`` subclass declaratively.

If ``assign`` is ``True`` and the default value is ever utilized, immediately pretend the default value was assigned to
this attribute.  (Override this in subclasses.)

3.5. CallbackAttribute
----------------------

An attribute that automatically executes the value upon retrieval, if a callable routine.

Frequently used by validation, transformation, and object mapper systems, especially as default value attributes.  E.g.
MongoEngine's ``choices`` argument to ``Field`` subclasses.

3.6. Attributes
---------------

A declarative attribute you can use in your own ``Container`` subclasses to provide views across the known attributes
of that container.  Can provide a filter (which uses ``isinstance``) to limit to specific attributes.

This is a dynamic property that generates an ``OrderedDict`` on each retrieval.  If you wish to use it frequently it 
would be prudent to make a more local-scope reference.


4. Validation
=============

Marrow Schema offers a wide variety of data validation primitives.  These are constructed declaratively where possible,
and participate in Marrow Schema's ``Element`` protocol as both ``Container`` and ``Attribute``.

You can create hybrid subclasses of individual validator classes to create basic compound validators.  Dedicated
compound validators are also provided which give more fine-grained control over how the child validators are executed.
A hybrid validator's behaviour will depend on the order of the parent classes.  It will execute the parent validators
until one fails, or all succeed.

4.1. Validation Basics
----------------------

Given an instance of a ``Validator`` subclass you simply call the ``validate`` method with the value to validate and
an optional execution context passed positionally, in that order.  The value, potentially transformed as required to
validate, is returned.  For example, the simple validator provided that always passes can be used like this::

    from marrow.schema.validation import always
    
    assert always.validate("Hello world!") == "Hello world!"

Writing your own validators can be as simple as subclassing ``Validator`` and overriding the ``validate`` method,
however there are other (more declarative) ways to create custom validators.

For now, though, we can write a validator that only accepts the number 27::

    from marrow.schema.validation import Concern, Validator
    
    class TwentySeven(Validator):
        def validate(self, value, context=None):
            if value != 27:
                raise Concern("Totally not twenty seven, dude.")
            return value
    
    validate = TwentySeven().validate
    
    assert validate(27) == 27
    validate(42)  # Boom!

You can see that validators should return the value if successful and raise an exception if not.  What if you want the
validator to be more generic, allowing you to define any arbitrary number to compare against::

    from marrow.schema import Attribute
    
    class Equals(Validator):
        value = Attribute()
        
        def validate(self, value, context=None):
            if value != self.value:
                raise Concern("Value of {0!r} doesn't match expectation of {1!r}.", value, self.value)
            
            return value
    
    validate = Equals(3).validate
    
    assert validate(3) == 3
    validate(27)  # Boom!

That's basically the built-in Equal validator, right there.  (You'll notice that it doesn't even care if the value is a
number or not.  Python is awesome that way.)

4.1.1. Concerns
~~~~~~~~~~~~~~~

Validators raise "concerns" if they encounter problems with the data being validated.  A ``Concern`` exception has a
level, identical to a logging level, and only errors (and above) should be treated as such.  This level defaults to
``logging.ERROR``.  Because most validation concerns should probably be fatal, overriding this value isn't done much
within Marrow Schema; it's mostly there for developer use.  Because of this, though, ``Concern`` has a somewhat strange
constructor::

    Concern([level, ]message, *args, concerns=[], **kw)

An optional integer logging level, then a message followed by zero or more additional arguments, an optional
``concerns`` keyword-only argument that is either not supplied or an iterable of child ``Concern`` instances, and zero
or more additional keyword arguments.  (The keyword-only business is enforced on both Python 2 and 3.)  Compound
validators that aggregate multiple failures (i.e. ``Pipe``) automatically determine their aggregate ``Concern`` level
from the maximum of the child concerns.

``Concern`` instances render to the native unicode type (``unicode`` in Python 2, ``str`` in Python 3) the result of
calling ``message.format(*args, **kw)`` using the arguments provided above.  Care should be taken to only include
JSON-safe datatypes in these arguments.


4.2. Basic Validators
---------------------

Marrow Schema includes a *lot* of validators for you to use.  They tend to be organized based on purpose, but the basic
validators have such widespread usage they're importable straight from ``marrow.schema.validation``.

* ``Validator`` — the base validator; a no-op.
* ``Always`` — effectively the same in effect as using Validator directly, always passes.  Singleton: ``always``
* ``Never`` — the opposite of Always, this never passes.  Singleton: ``never``
* ``AlwaysTruthy`` — the value must always evaluate to True.  Singleton: ``truthy``
* ``Truthy`` — A mixin-able version of AlwaysTruthy whose behaviour is toggled by the ``truthy`` attribute.
* ``AlwaysFalsy`` — as per AlwaysTruthy.  Singleton: ``falsy``
* ``Falsy`` — A mixin-able version of AlwaysFalsy, as per Truthy with the ``falsy`` attribute instead.
* ``AlwaysRequried`` — Value must be non-None.  Singleton: ``required``
* ``Required`` — A mixin-able version of AlwaysRequired using the ``required`` attribute.
* ``AlwaysMissing`` — Value must be None or otherwise have a length of zero.  Singleton: ``missing``
* ``Missing`` — A mixin-able version of AlwaysMissing using the ``missing`` attribute.
* ``Callback`` — Execute a simple callback to validate the value.  More on this one later.
* ``In`` — Value must be contained within the provided iterable, ``choices``.
* ``Contains`` — Value must contain (via ``in``) the provided value, ``contains``.
* ``Length`` — Value must have either an exact length or a length within a given range, ``length``.  (Hint: assign a tuple or a ``slice()``.)
* ``Range`` — Value must exist within a specific range (``minimum`` and ``maximum``) either end of which may be unbounded.
* ``Pattern`` — Value must match a regular expression, ``pattern``.  The expression will be compiled for you during assignment if passing in raw strings.
* ``Instance`` — Value must be an instance of the given class ``instance`` or an instance of one of a set of classes (by passing a tuple).
* ``Subclass`` — Value must be a subclass of the given class ``subclass`` or a subclass of one of a set of classes (by passing a tuple).
* ``Equal`` — Value must equal a given value, ``equals``.
* ``Unique`` — No element of the provided iterable value may be repeated.  Uses sets, so all values must also be hashable.  Singleton: ``unique``

4.3. Callback Validators
------------------------

Callback validators allow you to write validator logic using simple lambda statements, amongst other uses.  They
rapidly enter the realm of the spooky door when you realize the Callback validator class can be used as a decorator, though.  To see what we mean you could define the "Always" validator like this::

    from marrow.schema.validation import Callback
    
    @Callback
    def always(validator, value, context=None):
        return value
    
    assert always.validate(27) == 27

The callback that callback validators use may return a value, raise a Concern like any normal ``validate`` method, or
simply *return* a Concern instance which will then be raised on behalf of the callback.  The original callback function
is reachable as ``always.validator`` in this instance.

(If the decorator thing has you scratching your head, notice that the callback is assigned using an Attribute instance… and positional arguments fill out attributes!  Magic!)

4.4. Compound Validators
------------------------

Compound validators (imported from ``marrow.schema.validation.compound``) use other validators as declarative
attributes.  Additionally, you can pass validators at class instantiation time positionally or using the ``validators``
keyword argument.  Declarative child validators take priority.

The ``__validators__`` aggregate is provided to filter the known attributes of the ``Compound`` subclass to just the
assigned validators.  A generator property named ``_validators`` is provided to merge the two sources.

The purpose of this type of validator is to give you additional control over how multiple validators are run against a
single value, and how validators are run against collections (such as lists and dictionaries).

* ``Compound`` — The base class providing validator aggregation; effectively a no-op.
* ``Any`` — Stop processing on first success, but gather multiple failures into one.
* ``All`` — Ensure all validators pass, but stop processing on the first failure.  Does not gather failures.
* ``Pipe`` — Execute all validators and only declare success if all pass.  Gathers failures together.
* ``Iterable`` — Value must be an iterable whose elements pass validation using the base scheme defined by ``require``,
  generally one of ``Any``, ``All``, or ``Pipe``, but may be recursive.  (The class, not an instance of the class, or
  a ``functools.partial``-wrapped class for recursive use.)
* ``Mapping`` — Value must be a mapping (``dict``-like) whose values non-recursively validate using the base scheme
  defined by ``require``.  As per ``Iterable``, you can use ``functools.partial`` to build recursive compound
  validators.

4.5. Date and Time Validators
-----------------------------

* ``Date`` — A ``Range`` filter that only accepts datetime and date instances.
* ``Time`` — A ``Range`` filter that only accepts datetime and time instances.
* ``DateTime`` — A ``Range`` filter that only accepts datetime instances.
* ``Delta`` — A ``Range`` filter that only accepts timedelta instances.

4.6. Geographic Validators
--------------------------

All have singletons using the all-lower-case name.

* ``Latitude`` — A ``Compound`` validator ensuring the value is a number between -90 and 90 (degrees).
* ``Longitude`` — A ``Compound`` validator ensuring the value is a number between -180 and 180 (degrees).
* ``Position`` — A ``Compound`` validator ensuring the value is a sequence of length two whose first element is a valid
  latitude and whose second element is a valid longitude.

4.7. Network-Related Validators
-------------------------------

All have singletons using the all-lower-case name.  All are ``Pattern`` validators.

* ``IPv4`` — IPv4 dot-notation address.
* ``IPv4`` — IPv6 dot-notation address.
* ``CIDRv4`` — IPv4 network range.
* ``CIDRv6`` — IPv6 network range.
* ``IPAddress`` — An IPv4 *or* IPv6 address.
* ``CIDR`` — An IPv4 *or* IPv6 network range.
* ``Hostname`` — Valid ASCII host name validator.
* ``DNSName`` — Valid DNS RFC host name validator.
* ``MAC`` — Media Access Control (MAC) address validator.
* ``URI`` — Uniform Resource Locator (URI) validator.

4.8. Regular Expression Pattern Validators
------------------------------------------

These were not more specific to another task.  All are ``Pattern`` validators.  All have singletons using the
all-lower-case name.

* ``Alphanumeric`` — Case-insensitive letters and numbers.
* ``Username`` — Simple username validator: leading character must be alphabetical, subsequent characters may be alphanumeric, hyphen, period, or underscore.
* ``TwitterUsername`` — A validator for modern Twitter handles.
* ``FacebookUsername`` — A validator for modern Facebook usernames.
* ``CreditCard`` — A basic CC validator; does not validate checksum.
* ``HexColor`` — Hashmark color code of either three or six elements.  (Half-byte or full-byte RGB accuracy.)
* ``AlphaHexColor`` — Hashmark color code of either four or eight elements.  (Half-byte or full-byte RGBA accuracy.)
* ``ISBN`` — A very complete ISBN validator.
* ``Slug`` — Generally acceptable URL component validator.  Includes word characters, underscore, and hyphen.
* ``UUID`` — Basic UUID validation.  Accepts technically invalid UUIDs that are nontheless well-formed.

4.9. Utilities
--------------

* ``marrow.schema.validation:Validated`` — A mix-in for ``Attribute`` subclasses that performs validation on any
  attempt to assign a value.  Not useful by itself.
* ``marrow.schema.validation.util:SliceAttribute`` — Enforce a typecasting to a ``slice()`` instance by consuming
  iterables.
* ``marrow.schema.validation.util:RegexAttribute`` — Automatically attempt to ``re.compile`` objects that do not have a
  ``match`` method.

4.9.1 Testing
~~~~~~~~~~~~~

A helper class is provided to aid in testing your own validators.  It is a test generator allowing you to quickly and
easily define a validator and iterables of valid and invalid values to try.  This class is used extensively by Marrow
Schema itself and is agnostic to your preferred test runner.  (As long as the runner understands test generators.)

This utility class (``marrow.schema.validation.testing:ValidationTest``) has been tested under Nose and py.test.


5. Version History
==================

Version 1.0
-----------

* Initial release.

Version 1.0.1
-------------

* Compatibility with Python 2.6.

* Added pypy3 to test suite.

Version 1.0.2
-------------

* Callbacks are now provided to inform attributes when they are defined, and for containers when they likewise defined.

* If an attribute is overridden by a non-attribute value, it shouldn't be included in ``__attributes__`` and co.

* If an attribute is overridden by a new attribute, preserve the original definition order.  This is useful, as an
  example, to ensure the order of positional arguments don't change even if you override the default value through
  redefinition.

Version 1.1.0
-------------

* **Massive update to documentation.**  Now most lines of code are also covered by descriptive comments.

* **Validation primitives.**  A large component of this release is a newly added and fully tested suite of data
  validation tools.

* **Tests to Ludicrous Speed.**  Marrow Schema now has more individual tests (600+) than executable statements, and
  they execute in a few seconds on most interpreters!  Remember, kids: mad science is never stopping to ask "what's the
  worst that could happen?"

* **Expanded Travis coverage.**  Travis now runs the py26 and pypy3 test runners.

Version 1.1.1
-------------

* Removal of diagnostic aides.


6. License
==========

Marrow Schema has been released under the MIT Open Source license.

6.1. The MIT License
--------------------

Copyright © 2013-2015 Alice Bevan-McGregor and contributors.

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


.. |masterstatus| image:: http://img.shields.io/travis/marrow/schema/master.svg?style=flat
    :target: https://travis-ci.org/marrow/schema
    :alt: Release Build Status

.. |developstatus| image:: http://img.shields.io/travis/marrow/schema/develop.svg?style=flat
    :target: https://travis-ci.org/marrow/schema
    :alt: Development Build Status

.. |latestversion| image:: http://img.shields.io/pypi/v/marrow.schema.svg?style=flat
    :target: https://pypi.python.org/pypi/schema
    :alt: Latest Version

.. |downloads| image:: http://img.shields.io/pypi/dw/marrow.schema.svg?style=flat
    :target: https://pypi.python.org/pypi/schema
    :alt: Downloads per Week

.. |mastercover| image:: http://img.shields.io/coveralls/marrow/schema/master.svg?style=flat
    :target: https://travis-ci.org/marrow/schema
    :alt: Release Test Coverage

.. |developcover| image:: http://img.shields.io/coveralls/marrow/schema/develop.svg?style=flat
    :target: https://travis-ci.org/marrow/schema
    :alt: Development Test Coverage

.. |issuecount| image:: http://img.shields.io/github/issues/marrow/schema.svg?style=flat
    :target: https://github.com/marrow/schema/issues
    :alt: Github Issues

.. |cake| image:: http://img.shields.io/badge/cake-lie-1b87fb.svg?style=flat
