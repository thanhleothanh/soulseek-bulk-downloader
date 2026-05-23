import os


class Presenter:
    @staticmethod
    def _format_counts(responses, formats):
        counts = {fmt: 0 for fmt in formats}
        for r in responses:
            for f in r.get("files", []):
                ext = f.get("filename", "").lower().split(".")[-1]
                if ext in counts:
                    counts[ext] += 1
        return counts

    def songs_loaded(self, count, filepath):
        print(f"Loaded {count} songs from '{filepath}'. Starting quality-filtered scan...")

    def processing_concurrently(self, workers):
        print(f"Processing with {workers} concurrent workers...")

    def searching(self, song):
        print(f"[{song}] Searching...")

    def search_failed(self, song):
        print(f"[{song}] Failed to create search")

    def polling(self, song, timeout):
        print(f"[{song}] Waiting for results (up to {timeout}s)...")

    def no_results(self, song):
        print(f"[{song}] No results found within timeout")

    def stats(self, song, responses, formats):
        counts = self._format_counts(responses, formats)
        parts = " | ".join(f"{fmt.upper()}={counts[fmt]}" for fmt in formats)
        print(f"[{song}] {len(responses)} responses | {parts}")

    def no_match(self, song):
        print(f"[{song}] No matching file found")

    def found(self, song, username, file):
        filename = file.get("filename", "")
        basename = os.path.basename(filename)
        ext = filename.lower().split(".")[-1]
        bitrate = file.get("bitRate") or file.get("bitrate")
        print(f"[{song}] {ext.upper()} {basename} | bitrate={bitrate}")
        print(f"[{song}] Match: {basename} from '{username}'")

    def enqueued(self, song):
        print(f"[{song}] Enqueued!")

    def enqueue_failed(self, song, error):
        print(f"[{song}] Failed to enqueue: {error}")

    def checking_transfers(self):
        print("\nChecking transfer statuses...")

    def transfer_state(self, song, state):
        print(f"[{song}] Transfer state: {state}")

    def transfer_fetch_error(self, error):
        print(f"Failed to fetch transfers: {error}")

    def summary(self, successful, failed):
        print("\n" + "=" * 50)
        print("DOWNLOAD SUMMARY")
        print("=" * 50)
        print(f"Successfully enqueued ({len(successful)}):")
        for s in successful:
            print(f"  {s}")
        print(f"\nFailed to find/enqueue ({len(failed)}):")
        for f in failed:
            print(f"  {f}")
        print("=" * 50)
        print("\nScan complete! Check slskd Web UI at http://localhost:5030 to monitor download progress.")
