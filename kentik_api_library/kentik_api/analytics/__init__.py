try:
    import pandas as pd  # type: ignore
except ImportError:
    raise RuntimeError("Analytics support requires 'pandas'")
try:
    import yaml
except ImportError:
    raise RuntimeError("Analytics support requires 'pyyaml'")

from .data_frame_cache import DFCache
from .flatness import FlatnessResults, flatness_analysis
from .mapped_query import SQLQueryDefinition
