# Soulseek Bulk Downloader

A Docker-based bulk music downloader that searches and downloads tracks from the Soulseek network via [slskd](https://github.com/slskd/slskd).

## Features

- Bulk download from a list of songs in `songs.txt`
- Quality filter: accepts FLAC (any quality) or MP3 at 320kbps only
- Runs entirely in Docker with slskd

## Prerequisites

- Docker & Docker Compose

## Quick Start

1. Run the setup script (first time only):
   ```bash
   ./scripts/setup.sh
   ```

2. Create `.env` from the example file (optional, defaults are provided):
   ```bash
   cp .env.example .env
   ```

3. Create `songs.txt` from the example file:
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
   ./scripts/run.sh
   ```

3. Monitor progress:
   ```bash
   docker compose logs -f downloader
   ```

4. Access the slskd web UI at `http://localhost:5030` to check download status.

## Configuration

All settings are managed via `.env` at the project root. Copy `.env.example` to `.env` and adjust as needed.

### slskd Settings

Edit `slskd.yml` to configure your Soulseek username, password, and download directory.

### Quality Filter

Edit `.env` to change accepted MP3 bitrates:

```
TARGET_BITRATES=320,256
```

Leave it blank (`TARGET_BITRATES=`) to accept all MP3 bitrates. FLAC files are always accepted regardless of this setting.

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SLSKD_HOST` | `http://slskd:5030` | slskd API endpoint |
| `SLSKD_API_KEY` | `none` | API key (if enabled in slskd) |
| `TARGET_BITRATES` | `320` | Comma-separated MP3 bitrates to accept (blank = all) |
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
├── slskd-data/             # slskd persistent data
├── scripts/
│   ├── setup.sh            # One-time setup (creates required folders)
│   ├── run.sh              # Start/rebuild and run the downloader
│   ├── clean-up.sh         # Stop containers and wipe data
│   └── flatten-downloads.sh # Flatten downloaded files
└── src/
    ├── main.py             # Main download script
    ├── searcher.py         # Song search logic
    ├── client.py           # Thread-safe slskd API wrapper
    └── tracker.py          # Transfer status verification
```

## Notes

- The downloader waits 15 seconds after each search to collect results from the network
- Downloads are saved to the `./downloads` directory
- slskd API key authentication is disabled by default in this setup

## Cleanup

To stop containers and remove all downloads and slskd data:

```bash
./scripts/clean-up.sh
```
