import logging

import pykka
from mopidy import backend

from .client import RadioPitClient
from .library import RadioPitLibraryProvider, STATION_URI_PREFIX

logger = logging.getLogger(__name__)


class RadioPitBackend(pykka.ThreadingActor, backend.Backend):
    uri_schemes = ["radiopit"]

    def __init__(self, config, audio):
        super().__init__()
        cfg = config["radiopit"]
        self._client = RadioPitClient(
            api_url=cfg["api_url"],
            api_key=cfg["api_key"],
        )
        self.library = RadioPitLibraryProvider(backend=self)
        self.playback = RadioPitPlaybackProvider(audio=audio, backend=self)

    def on_start(self):
        logger.info("RadioPit backend started")

    def on_stop(self):
        logger.info("RadioPit backend stopped")


class RadioPitPlaybackProvider(backend.PlaybackProvider):
    def translate_uri(self, uri):
        if not uri.startswith(STATION_URI_PREFIX):
            return None
        station_id = uri[len(STATION_URI_PREFIX):]
        station = self.backend._client.get_station(station_id)
        if station:
            logger.debug("Resolving %s -> %s", uri, station["url"])
            return station["url"]
        logger.warning("Station not found for URI: %s", uri)
        return None
