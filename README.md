# Soulseek Bulk Downloader

A Docker-based bulk music downloader that searches and downloads tracks from the Soulseek network via [slskd](https://github.com/slskd/slskd).

## Features

- Bulk download from a list of songs in `songs.txt`
- Quality filter: accepts FLAC (any quality) or MP3 at 320kbps only
- Runs entirely in Docker with slskd

## Prerequisites

- Docker & Docker Compose

## Quick Start

1. Create `songs.txt` from the example file:
   ```bash
   cp songs.txt.example songs.txt
   ```

2. Add your song queries to `songs.txt` (one per line):
   ```
   vertigo kisnou
   a breath of fresh air danisogen
   ```

3. Start the services:
   ```bash
   ./run.sh
   ```

3. Monitor progress:
   ```bash
   docker compose logs -f downloader
   ```

4. Access the slskd web UI at `http://localhost:5030` to check download status.

## Configuration

### slskd Settings

Edit `slskd.yml` to configure your Soulseek username, password, and download directory.

### Quality Filter

Edit `downloader/bulk_download.py` to change the quality filter:

```python
TARGET_FORMATS = [".mp3", ".flac"]
TARGET_BITRATE = 320
```

Current logic: accept FLAC (any quality) OR MP3 at exactly 320kbps.

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SLSKD_HOST` | `http://slskd:5030` | slskd API endpoint |
| `SLSKD_API_KEY` | `none` | API key (if enabled in slskd) |

## File Structure

```
.
├── docker-compose.yml      # Docker services definition
├── slskd.yml               # slskd configuration
├── songs.txt               # List of songs to search (one per line)
├── songs.txt.example       # Example template for songs.txt
├── downloads/              # Downloaded files
├── slskd-data/             # slskd persistent data
└── downloader/
    ├── Dockerfile
    ├── bulk_download.py    # Main download script
    └── requirements.txt    # Python dependencies
```

## Notes

- The downloader waits 15 seconds after each search to collect results from the network
- Downloads are saved to the `./downloads` directory
- slskd API key authentication is disabled by default in this setup

## Cleanup

To stop containers and remove all downloads and slskd data:

```bash
./clean-up.sh
```
