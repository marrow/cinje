# encoding: utf-8

from .release import version as __version__

# ## Primary API Entry Points

from .encoding import transform
from .util import stream, flatten, fragment
