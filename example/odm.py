# encoding: utf-8

from __future__ import unicode_literals

from decimal import Decimal as decimal, ROUND_HALF_UP
from marrow.schema.declarative import nil, Container, Attribute
from marrow.schema.util import Attributes
from marrow.util.url import URL as url
from marrow.util.convert import boolean
from bson import ObjectId


class ValidationError(Exception):
    pass


# Field transformations.
# These provide an API for conversions between database and Python data structures.
# "Settings" can be added by attaching Attribute instances.

class Transform(Container):
    """Convert a value between Python-native and database-friendly datatypes."""
    
    def __call__(self, value):
        """Get the database-friendly version of this Python-native value."""
        return value
    
    def native(self, value):
        """Get the Python-native version of this web-friendly value."""
        return value


class NaiveTransform(Transform):
    """Primarily useful for base types such as str, unicode, int, etc.
    
    An example of a Transform subclass with settings.
    """
    
    kind = Attribute(default=unicode)
    
    def __call__(self, value):
        return self.kind(value)
    
    def native(self, value):
        return self.kind(value)


class URLTransform(Transform):
    def __call__(self, value):
        return unicode(value)
    
    def native(self, value):
        return url(value)


class DecimalTransform(Transform):
    def __call__(self, value):
        return unicode(value)
    
    def native(self, value):
        return Decimal(value)


# Core field definition.
# Contains the basic attributes common to all fields.

class Field(Attribute):
    required = Attribute(default=False)
    unique = Attribute(default=False)
    primary = Attribute(default=False)
    transform = Attribute(default=Transform())
    validator = Attribute(default=None)
    choices = Attribute(default=None)
    
    def __init__(self, *args, **kw):
        super(Field, self).__init__(*args, **kw)
        
        # Fields that aren't required naturally default to None.
        if not self.required:
            try:
                self.default
            except AttributeError:
                self.default = None
    
    def __set__(self, obj, value):
        try:
            self.default
        except AttributeError:
            pass
        else:
            if value is self.default:
                del obj[self._key]
                return
        
        if self.required and value in (None, nil):
            raise ValidationError("Required fields can not be empty or omitted.")
        
        if self.choices and value not in self.choices:
            raise ValidationError("Value not in allowed range.")
        
        if self.validator: self.validator(value)
        
        super(Field, self).__set__(obj, value)
    
    def __delete__(self, obj):
        if self.required:
            raise ValidationError()
        
        super(Field, self).__del__(obj)


# Some samples.

class Identifier(Field):
    transform = Attribute(default=NaiveTransform(ObjectId))


class String(Field):
    transform = Attribute(default=NaiveTransform(unicode))
    regex = Attribute(default=None)


class URL(String):
    transform = Attribute(default=URLTransform())
    verify = Attribute(default=False)  # Perform a requests.head call to validate existence.


class Number(Field):
    transform = Attribute(default=NaiveTransform(int))


class Float(Field):
    transform = Attribute(default=NaiveTransform(float))
    minimum = Attribute(default=None)
    maximum = Attribute(default=None)


class Decimal(Float):
    transform = Attribute(default=DecimalTransform())
    rounding = Attribute(defualt=ROUND_HALF_UP)


class Boolean(Field):
    transform = Attribute(default=NaiveTransform(boolean))


class DateTime(Field):
    accurate = Attribute(default=False)  # Microsecond accurate?


class Dynamic(Field):
    pass


class List(Field):
    contains = Attribute()


class Dictionary(Field):
    pass


class Mapping(Field):
    contains = Attribute()


class Reference(Field):
    to = Attribute(default=None)
    policy = Field(choices=(None, 'deny', 'nullify', 'cascade', 'pull'))


class Binary(Field):
    pass


class File(Binary):
    collection = Field(default='fs')


class Image(File):
    pass


class UUID(Field):
    binary = Attribute(default=True)


class Point(Field):
    pass


class PointLine(Field):
    pass


class Polygon(Field):
    pass


class GridFilesystem(Field):
    pass


class ImageGridFilesystem(GridFilesystem):
    pass


# Basic document class.
# Pretend this has accessors for 'objects' (the queryset) etc.

class Document(Container):
    __fields__ = Attributes(Field)


# The actual sample follows.

class SampleDocument(Document):
    name = String(required=True)
    age = Number(maximum=130)


print(SampleDocument.__fields__)

instance = SampleDocument("Alice", 27)
print(instance.__data__)
