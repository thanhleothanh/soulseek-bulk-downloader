import threading
from slskd_api import SlskdClient


class ThreadSafeClient:
    def __init__(self, host, api_key):
        self._client = SlskdClient(host=host, api_key=api_key)
        self._lock = threading.Lock()

    def search_text(self, song_query):
        with self._lock:
            return self._client.searches.search_text(song_query)

    def search_responses(self, search_id):
        with self._lock:
            return self._client.searches.search_responses(search_id)

    def enqueue(self, username, files):
        with self._lock:
            return self._client.transfers.enqueue(username=username, files=files)

    def get_all_downloads(self):
        with self._lock:
            return self._client.transfers.get_all_downloads()
