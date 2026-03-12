import logging

import requests

logger = logging.getLogger(__name__)


class RadiopitClient:
    def __init__(self, api_url, api_key):
        self._api_url = api_url.rstrip("/")
        self._session = requests.Session()
        self._session.headers.update({"x-api-key": api_key})

    def get_playlists(self):
        try:
            r = self._session.get(f"{self._api_url}/api/playlists", timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            logger.error("Failed to fetch playlists: %s", e)
            return []

    def get_stations(self):
        try:
            r = self._session.get(f"{self._api_url}/api/stations", timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            logger.error("Failed to fetch stations: %s", e)
            return []

    def get_station(self, station_id):
        stations = self.get_stations()
        for s in stations:
            if s["_id"] == station_id:
                return s
        return None
