"""Bronze assets package initialization."""

# Import asset modules
try:
    from . import run_bronze_example

    _bronze_example_imported = True
except ImportError:
    _bronze_example_imported = False

__all__ = ["run_bronze_example"] if _bronze_example_imported else []
