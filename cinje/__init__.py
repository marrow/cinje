# encoding: utf-8

from .release import version as __version__
# from .encoding import Translator, transform

from .block import Function, Generic, Module, Using
from .inline import Blank, Code, Comment, Flush, Text, Use

from .encoding import transform
