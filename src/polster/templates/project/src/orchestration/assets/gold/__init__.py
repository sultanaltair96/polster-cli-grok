"""Gold assets package initialization."""

# Import asset modules
try:
    from . import run_gold_example

    _gold_example_imported = True
except ImportError:
    _gold_example_imported = False

__all__ = ["run_gold_example"] if _gold_example_imported else []
