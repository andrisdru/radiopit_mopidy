import pathlib

from mopidy import config, ext

__version__ = "1.0.9"


class Extension(ext.Extension):
    dist_name = "Mopidy-RadioPit"
    ext_name = "radiopit"
    version = __version__

    def get_default_config(self):
        return config.read(pathlib.Path(__file__).parent / "ext.conf")

    def get_config_schema(self):
        schema = super().get_config_schema()
        schema["api_key"] = config.String()
        schema["api_url"] = config.String()
        return schema

    def setup(self, registry):
        from .actor import RadioPitBackend

        registry.add("backend", RadioPitBackend)
