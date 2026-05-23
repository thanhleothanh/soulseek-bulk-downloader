import time

SEARCH_POLL_INTERVAL = 10
SEARCH_TIMEOUT = 100


class SongSearcher:
    def __init__(self, client):
        self._client = client

    def search(self, song_query):
        try:
            search_job = self._client.search_text(song_query)
            return search_job.get("id")
        except Exception:
            return None

    def poll_results(self, search_id):
        for _ in range(SEARCH_TIMEOUT // SEARCH_POLL_INTERVAL):
            time.sleep(SEARCH_POLL_INTERVAL)
            try:
                responses = self._client.search_responses(search_id)
            except Exception:
                return None
            if responses:
                return responses
        return None
