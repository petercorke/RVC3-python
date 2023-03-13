try:
    import importlib.metadata
    __version__ = importlib.metadata.version("rvc3python")
except:
    pass