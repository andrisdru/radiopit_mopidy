import logging

from mopidy import backend
from mopidy.models import Album, Artist, Image, Ref, Track

logger = logging.getLogger(__name__)

ROOT_URI = "radiopit:root"
PLAYLIST_URI_PREFIX = "radiopit:playlist:"
STATION_URI_PREFIX = "radiopit:station:"

RADIOPIT_ICON = "https://radiopit.drulle.lv/icons/icon-192.png"


def playlist_uri(playlist_id):
    return f"{PLAYLIST_URI_PREFIX}{playlist_id}"


def station_uri(station_id):
    return f"{STATION_URI_PREFIX}{station_id}"


class RadiopitLibraryProvider(backend.LibraryProvider):
    root_directory = Ref.directory(uri=ROOT_URI, name="Radiopit")

    def __init__(self, backend):
        super().__init__(backend)
        self._client = backend._client

    def browse(self, uri):
        if uri == ROOT_URI:
            return self._browse_root()
        if uri.startswith(PLAYLIST_URI_PREFIX):
            playlist_id = uri[len(PLAYLIST_URI_PREFIX):]
            return self._browse_playlist(playlist_id)
        return []

    def _browse_root(self):
        playlists = self._client.get_playlists()
        stations = self._client.get_stations()

        refs = []
        for pl in sorted(playlists, key=lambda x: x.get("order", 0)):
            refs.append(
                Ref.directory(uri=playlist_uri(pl["_id"]), name=pl["name"])
            )

        unassigned = [s for s in stations if not s.get("playlistId")]
        if unassigned:
            refs.append(
                Ref.directory(uri=playlist_uri("unassigned"), name="Unassigned")
            )

        return refs

    def _browse_playlist(self, playlist_id):
        stations = self._client.get_stations()

        if playlist_id == "unassigned":
            filtered = [s for s in stations if not s.get("playlistId")]
        else:
            filtered = [s for s in stations if s.get("playlistId") == playlist_id]

        filtered = sorted(filtered, key=lambda x: x.get("order", 0))
        return [Ref.track(uri=station_uri(s["_id"]), name=s["name"]) for s in filtered]

    def lookup(self, uri):
        if not uri.startswith(STATION_URI_PREFIX):
            return []
        station_id = uri[len(STATION_URI_PREFIX):]
        station = self._client.get_station(station_id)
        if station:
            return [_station_to_track(station)]
        return []

    def get_images(self, uris):
        logger.debug("get_images called with %d URIs: %s", len(uris), uris)
        result = {}
        stations = None

        for uri in uris:
            if uri == ROOT_URI:
                result[uri] = [Image(uri=RADIOPIT_ICON)]

            elif uri.startswith(PLAYLIST_URI_PREFIX):
                result[uri] = [Image(uri=RADIOPIT_ICON)]

            elif uri.startswith(STATION_URI_PREFIX):
                if stations is None:
                    stations = self._client.get_stations()
                station_id = uri[len(STATION_URI_PREFIX):]
                for s in stations:
                    if s["_id"] == station_id:
                        icon_url = s.get("iconUrl") or RADIOPIT_ICON
                        result[uri] = [Image(uri=icon_url)]
                        logger.debug("Image for %s: %s", uri, icon_url)
                        break

        return result

    def search(self, query=None, uris=None, exact=False):
        return None


def _station_to_track(station):
    name = station["name"]
    return Track(
        uri=station_uri(station["_id"]),
        name=name,
        artists=[Artist(name=name)],
        album=Album(name="Radiopit"),
        length=None,
    )
