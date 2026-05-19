import time


TRANSFER_CHECK_DELAY = 10
SUCCESS_STATES = {
    "Initializing",
    "InProgress",
    "Completed, Succeeded",
}


class ResultTracker:
    def __init__(self, client):
        self._client = client

    def verify_transfers(self, enqueued, failed_to_enqueue):
        print("\n⏳ Checking transfer statuses...")
        time.sleep(TRANSFER_CHECK_DELAY)

        final_successful = []
        final_failed = list(failed_to_enqueue)

        try:
            all_transfers = self._client.get_all_downloads()
            transfer_map = self._build_transfer_map(all_transfers)

            for song, info in enqueued.items():
                key = (info["username"], info["filename"])
                state = transfer_map.get(key, "Unknown")

                if state in SUCCESS_STATES:
                    final_successful.append(song)
                else:
                    final_failed.append(song)
                    print(f"[{song}] ⚠️ Transfer state: {state}")
        except Exception as e:
            print(f"❌ Failed to fetch transfers: {e}")
            final_successful = list(enqueued.keys())
            final_failed.extend(final_successful)

        return final_successful, final_failed

    def _build_transfer_map(self, all_transfers):
        transfer_map = {}
        for t in all_transfers:
            u = t.get("username")
            for d in t.get("directories", []):
                for f in d.get("files", []):
                    if f.get("direction") == "Download":
                        key = (u, f.get("filename"))
                        transfer_map[key] = f.get("state")
        return transfer_map
