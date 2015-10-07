# encoding: utf-8

from .release import version as __version__
# from .encoding import Translator, transform

from .block import Conditional, Function, Iterator, Module, Using
from .inline import Blank, Code, Comment, Flush, Text

from .encoding import transform
