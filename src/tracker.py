import time

TRANSFER_CHECK_DELAY = 10
DEFAULT_SUCCESS_STATES = {
    "Initializing",
    "InProgress",
    "Completed, Succeeded",
}


class ResultTracker:
    def __init__(self, client):
        self._client = client

    def verify_transfers(self, presenter, enqueued, failed_to_enqueue=None):
        presenter.checking_transfers()
        time.sleep(TRANSFER_CHECK_DELAY)

        successful = []
        failed = list(failed_to_enqueue) if failed_to_enqueue else []

        try:
            all_transfers = self._client.get_all_downloads()
            transfer_map = self._build_transfer_map(all_transfers)

            for song, info in enqueued.items():
                key = (info["username"], info["filename"])
                state = transfer_map.get(key, "Unknown")
                if state in DEFAULT_SUCCESS_STATES:
                    successful.append(song)
                else:
                    failed.append(song)
                    presenter.transfer_state(song, state)

            return successful, failed
        except Exception as e:
            presenter.transfer_fetch_error(e)
            return list(enqueued.keys()), failed + list(enqueued.keys())

    @staticmethod
    def _build_transfer_map(all_transfers):
        transfer_map = {}
        for t in all_transfers:
            username = t.get("username")
            for d in t.get("directories", []):
                for f in d.get("files", []):
                    if f.get("direction") == "Download":
                        key = (username, f.get("filename"))
                        transfer_map[key] = f.get("state")
        return transfer_map
