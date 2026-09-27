# TaRenNG

Based on my experiences with the origin [TaRen][url_taren] and the AI crap I'm highly motivated to do a complete rewrite. Of course with some new ideas. And with support of AI for minor parts.

## The process

- Startup the program
- Check, if the movie collection folder exists (see config option "app"/"collection_root"). If the folder does not exist, abort the program.
- Ensure required infrastructure folders exists. Try to create them if they do not exist (see `tarenng/collection.py`).
- Mark all folders except the `unseen` folder with `.ignore` file - this folders excluded from [Jellyfin's][url_jellyfin] search index.

## The config options

The configuration is stored in `tarenng.json` next to the application. The file is
created automatically on first startup.

### `app`

| Option            | Default                                                                         | Description                                                                                          |
| ----------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `cache_age`       | `6`                                                                             | Maximum age of the web cache in days before it is refreshed.                                         |
| `cache_file`      | `<application directory>/collection/tarenng.html`                               | Path to the cached scraper response.                                                                 |
| `collection_root` | `<application directory>/collection`                                            | Root directory containing the movie collection. The program aborts if this directory does not exist. |
| `scraper_agent`   | `TaRenNG/0.0 (https://github.com/ThirtySomething/TaRenNG/) generic-library/0.0` | User-agent string sent when retrieving scraper data.                                                 |
| `scraper_source`  | `https://de.wikipedia.org/wiki/Liste_der_Tatort-Folgen`                         | URL used as the scraper source.                                                                      |
| `trash_age`       | `6`                                                                             | Maximum age of items in the trash folder before they are cleaned up.                                 |

### `logging`

| Option     | Default | Description                                                                                   |
| ---------- | ------- | --------------------------------------------------------------------------------------------- |
| `loglevel` | `info`  | Logging level used by the application logger, such as `debug`, `info`, `warning`, or `error`. |

Example:

```json
{
  "APP": {
    "cache_age": 6,
    "cache_file": "V:\\Tatort\\tarenng.html",
    "collection_root": "V:\\Tatort",
    "scraper_agent": "TaRenNG/0.0 (https://github.com/ThirtySomething/TaRenNG/) generic-library/0.0",
    "scraper_source": "https://de.wikipedia.org/wiki/Liste_der_Tatort-Folgen",
    "trash_age": 6
  },
  "LOGGING": {
    "loglevel": "debug"
  }
}
```

[url_jellyfin]: https://jellyfin.org/
[url_taren]: https://www.github.com/ThirtySomething/TaRen
