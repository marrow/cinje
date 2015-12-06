# encoding: utf-8

import pytest

from cinje import fragment, flatten


CODE = """
: def _wrapper
prefix
: yield
postfix
: end

: def consumer
: using _wrapper
content
: end
: end
"""

@pytest.fixture
def tmpl():
	return fragment(CODE)


def test_using(tmpl):
	assert flatten(tmpl()) == "prefix\ncontent\npostfix\n"

