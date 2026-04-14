"""BioPress Designer - Educational content generation tool."""

try:
    from importlib.metadata import version
    __version__ = version("biopress")
except Exception:
    __version__ = "0.1.0"
