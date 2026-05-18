import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import TEXT_FILE_PATH, MAX_WORKERS
from client import ThreadSafeClient
from searcher import SongSearcher
from tracker import ResultTracker


def load_songs():
    if not os.path.exists(TEXT_FILE_PATH):
        print(f"❌ Error: File '{TEXT_FILE_PATH}' not found in container.")
        print(f"   Please create a 'songs.txt' file from 'songs.txt.example' and mount it into the container.")
        sys.exit(1)

    with open(TEXT_FILE_PATH, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def print_summary(successful, failed):
    print("\n" + "=" * 50)
    print("📊 DOWNLOAD SUMMARY")
    print("=" * 50)
    print(f"✅ Successfully enqueued ({len(successful)}):")
    for s in successful:
        print(f"{s}")
    print(f"\n❌ Failed to find/enqueue ({len(failed)}):")
    for f in failed:
        print(f"{f}")
    print("=" * 50)
    print("\n🎉 Scan complete! Check slskd Web UI at http://localhost:5030 to monitor download progress.")


def main():
    songs = load_songs()
    print(f"📋 Loaded {len(songs)} songs from '{TEXT_FILE_PATH}'. Starting FLAC or MP3 320kbps scan...")

    client = ThreadSafeClient(
        host=os.environ.get("SLSKD_HOST", "http://localhost:5030"),
        api_key=os.environ.get("SLSKD_API_KEY", "none")
    )
    searcher = SongSearcher(client)
    tracker = ResultTracker(client)

    enqueued = {}
    failed_to_enqueue = []
    lock = threading.Lock()

    def process_song(song):
        result = searcher.search(song)
        if result:
            with lock:
                enqueued[song] = result
        else:
            with lock:
                failed_to_enqueue.append(song)

    print(f"🧵 Processing {MAX_WORKERS} songs concurrently...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_song, song) for song in songs]
        for future in as_completed(futures):
            future.result()

    final_successful, final_failed = tracker.verify_transfers(enqueued, failed_to_enqueue)
    print_summary(final_successful, final_failed)


if __name__ == "__main__":
    main()
