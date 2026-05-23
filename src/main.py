import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from client import ThreadSafeClient
from searcher import SongSearcher, SEARCH_TIMEOUT
from matcher import FileMatcher, DEFAULT_FORMAT_PRIORITY
from tracker import ResultTracker
from presenter import Presenter

TEXT_FILE_PATH = os.environ.get("SONGS_FILE", "songs.txt")
MAX_WORKERS = int(os.environ.get("MAX_WORKERS", "10"))
SLSKD_HOST = os.environ.get("SLSKD_HOST", "http://localhost:5030")
SLSKD_API_KEY = os.environ.get("SLSKD_API_KEY", "none")


def load_songs():
    if not os.path.exists(TEXT_FILE_PATH):
        print(f"Error: File '{TEXT_FILE_PATH}' not found.")
        print(f"Please create a 'songs.txt' file from 'songs.txt.example'.")
        sys.exit(1)

    with open(TEXT_FILE_PATH, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def main():
    client = ThreadSafeClient(host=SLSKD_HOST, api_key=SLSKD_API_KEY)
    presenter = Presenter()
    searcher = SongSearcher(client)
    matcher = FileMatcher()
    tracker = ResultTracker(client)

    songs = load_songs()
    presenter.songs_loaded(len(songs), TEXT_FILE_PATH)

    enqueued = {}
    failed_to_enqueue = []
    lock = threading.Lock()

    def process_song(song):
        presenter.searching(song)

        search_id = searcher.search(song)
        if search_id is None:
            presenter.search_failed(song)
            with lock:
                failed_to_enqueue.append(song)
            return

        presenter.polling(song, SEARCH_TIMEOUT)
        responses = searcher.poll_results(search_id)
        if responses is None:
            presenter.no_results(song)
            with lock:
                failed_to_enqueue.append(song)
            return

        presenter.stats(song, responses, DEFAULT_FORMAT_PRIORITY)

        match = matcher.find_best(responses)
        if match is None:
            presenter.no_match(song)
            with lock:
                failed_to_enqueue.append(song)
            return

        username, file = match
        presenter.found(song, username, file)

        try:
            client.enqueue(username=username, files=[{
                "id": file.get("id"),
                "filename": file.get("filename", ""),
                "size": file.get("size", 0),
            }])
            presenter.enqueued(song)
            with lock:
                enqueued[song] = {"username": username, "filename": file["filename"]}
        except Exception as e:
            presenter.enqueue_failed(song, e)
            with lock:
                failed_to_enqueue.append(song)

    presenter.processing_concurrently(MAX_WORKERS)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_song, song) for song in songs]
        for future in as_completed(futures):
            future.result()

    final_successful, final_failed = tracker.verify_transfers(presenter, enqueued, failed_to_enqueue)
    presenter.summary(final_successful, final_failed)


if __name__ == "__main__":
    main()
