"""Support for single-function template modules.

This is the Python equivalent of spooky action at a distance. When imported, modules utilizing this will swap
themselves in `sys.path` for the template function produced named `template`.

Syntax:

	: args [<argspec>]
"""