"""Silver assets package initialization."""

# Import asset modules
try:
    from . import run_silver_example

    _silver_example_imported = True
except ImportError:
    _silver_example_imported = False

__all__ = ["run_silver_example"] if _silver_example_imported else []
