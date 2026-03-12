# Mopidy-Radiopit

[![PyPI version](https://badge.fury.io/py/Mopidy-Radiopit.svg)](https://pypi.org/project/Mopidy-Radiopit/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Mopidy extension that exposes your [Radiopit](https://radiopit.drulle.lv) playlists and stations for browsing and playback. Works with Iris and other Mopidy web clients.

## Installation

Install from PyPI:

```bash
pip install Mopidy-Radiopit
```

## Requirements

- Python >= 3.9
- Mopidy >= 3.0
- Pykka >= 2.0
- requests >= 2.0

## Configuration

Add to your `mopidy.conf`:

```ini
[radiopit]
enabled = true
api_key = YOUR_API_KEY_HERE
api_url = https://radiopit-api.drulle.lv
```

Get your API key from the Radiopit web or Android app (Settings → API Key).

## Usage

In Iris (or any Mopidy browse client):

1. Open **Browse**
2. Click **Radiopit**
3. Your playlists appear as folders
4. Click a folder to see stations — click a station to play

## Project structure

```
mopidy_radiopit/
├── __init__.py   # Extension entry point
├── actor.py      # Backend + playback provider
├── client.py     # HTTP client for Radiopit API
├── library.py    # Browse/lookup library provider
└── ext.conf      # Default config values
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
```
