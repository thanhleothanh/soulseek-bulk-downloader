# Soulseek Bulk Downloader

A Docker-based bulk music downloader that searches and downloads tracks from the Soulseek network via [slskd](https://github.com/slskd/slskd).

## Features

- Bulk download from a list of songs in `songs.txt`
- Quality filter: prioritizes MP3 (320→256→192→128 kbps) > M4A > FLAC
- Runs entirely in Docker with slskd

## Prerequisites

- Docker & Docker Compose

## Quick Start

1. Run the setup script (first time only):
   ```bash
   ./setup.sh
   ```

2. Create `.env` from the example file (optional, defaults are provided):
   ```bash
   cp .env.example .env
   ```

3. Create `songs.txt` from the example file:
   ```bash
   cp songs.txt.example songs.txt
   ```

4. Add your song queries to `songs.txt` (one per line):
   ```
   vertigo kisnou
   a breath of fresh air danisogen
   ```

5. Start the services:
   ```bash
   ./run.sh
   ```

6. Monitor progress:
   ```bash
   docker compose logs -f downloader
   ```

7. Access the slskd web UI at `http://localhost:5030` to check download status.

## Configuration

All settings are managed via `.env` at the project root. Copy `.env.example` to `.env` and adjust as needed.

### slskd Settings

Edit `slskd.yml` to configure your Soulseek username, password, and download directory.

### Quality Filter

Accepts MP3 (320→256→192→128 kbps), then M4A, then FLAC. Hardcoded in `searcher.py`.

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SLSKD_HOST` | `http://slskd:5030` | slskd API endpoint |
| `SLSKD_API_KEY` | `none` | API key (if enabled in slskd) |
| `MAX_WORKERS` | `10` | Concurrent song searches |

## File Structure

```
.
├── docker-compose.yml      # Docker services definition
├── slskd.yml               # slskd configuration
├── .env                    # Environment configuration (create from .env.example)
├── .env.example            # Example template for .env
├── songs.txt               # List of songs to search (one per line)
├── songs.txt.example       # Example template for songs.txt
├── Dockerfile              # Docker image definition
├── requirements.txt        # Python dependencies
├── downloads/              # Downloaded files
├── logs/                   # Downloader logs
├── setup.sh                # One-time setup (creates required folders)
├── run.sh                  # Start/rebuild and run the downloader
├── clean-up.sh             # Stop containers and wipe data
├── flatten-downloads.sh    # Flatten downloaded files to a single directory
├── find-duplicates.sh      # Find potential duplicate files by duration
├── flac-to-mp3.sh          # Convert FLAC to MP3 (320kbps)
├── ogg-to-mp3.sh           # Convert OGG to MP3 (320kbps)
└── src/
    ├── main.py             # Main download script
    ├── searcher.py         # Song search logic
    ├── client.py           # Thread-safe slskd API wrapper
    ├── tracker.py          # Transfer status verification
    └── wait-for-slskd.py   # Waits for slskd to be ready before starting
```

## Notes

- The downloader polls for search results every 10s (up to 100s) to collect responses from the network
- Waits for slskd to be logged in before starting searches (120s timeout)
- Downloads are saved to the `./downloads` directory
- slskd API key authentication is disabled by default in this setup
- slskd is configured for download-only: no shared directories, distributed network disabled, minimal upload slots
- Resource limits are set for slskd (1 CPU, 1GB RAM) to prevent OOM crashes

## Cleanup

To stop containers and remove all downloads and slskd data:

```bash
./clean-up.sh
```
