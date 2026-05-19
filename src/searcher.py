import os
import time


TARGET_BITRATES_RAW = os.environ.get("TARGET_BITRATES", "320").strip()
TARGET_BITRATES = [int(x) for x in TARGET_BITRATES_RAW.split(",") if x.strip()] if TARGET_BITRATES_RAW else []
SEARCH_WAIT_SECONDS = 15


class SongSearcher:
    def __init__(self, client):
        self._client = client

    def search(self, song_query):
        print(f"[{song_query}] 🔍 Searching...")
        try:
            search_job = self._client.search_text(song_query)
            search_id = search_job.get("id")
        except Exception as e:
            print(f"[{song_query}] ❌ Failed to create search: {e}")
            return None

        print(f"[{song_query}] ⏳ Waiting {SEARCH_WAIT_SECONDS}s for results...")
        time.sleep(SEARCH_WAIT_SECONDS)

        try:
            responses = self._client.search_responses(search_id)
        except Exception as e:
            print(f"[{song_query}] ❌ Failed to get results: {e}")
            return None

        if not responses:
            print(f"[{song_query}] ⚠️ No results found")
            return None

        format_counts = {"mp3": 0, "flac": 0, "m4a": 0}
        for r in responses:
            for f in r.get("files", []):
                ext = f.get("filename", "").lower().split(".")[-1]
                if ext in format_counts:
                    format_counts[ext] += 1

        print(f"[{song_query}] 📊 {len(responses)} responses | FLAC={format_counts['flac']}, MP3={format_counts['mp3']}, M4A={format_counts['m4a']}")

        result = self._find_matching_file(responses, song_query)
        if result:
            return result

        print(f"[{song_query}] ❌ No matching file found")
        return None

    def _find_matching_file(self, responses, song_query):
        result = self._try_enqueue(responses, song_query, lambda ext, br: ext == "m4a")
        if result:
            return result

        for target_br in TARGET_BITRATES:
            result = self._try_enqueue(responses, song_query, lambda ext, br, t=target_br: ext == "mp3" and br == t)
            if result:
                return result

        if not TARGET_BITRATES:
            result = self._try_enqueue(responses, song_query, lambda ext, br: ext == "mp3")
            if result:
                return result

        result = self._try_enqueue(responses, song_query, lambda ext, br: ext == "flac")
        if result:
            return result

        return None

    def _try_enqueue(self, responses, song_query, match_fn):
        for response in responses:
            username = response.get("username")
            files = response.get("files", [])

            for file in files:
                file_filename = file.get("filename", "")
                file_id = file.get("id")
                file_size = file.get("size", 0)
                file_bitrate = file.get("bitRate") or file.get("bitrate")

                file_ext = file_filename.lower().split(".")[-1]
                if not match_fn(file_ext, file_bitrate):
                    continue

                if file_ext in ["mp3", "flac", "m4a"]:
                    print(f"[{song_query}] 📄 {file_ext.upper()} {os.path.basename(file_filename)} | bitrate={file_bitrate}")

                print(f"[{song_query}] ✅ Match: {os.path.basename(file_filename)} from '{username}'")

                try:
                    file_payload = {
                        "id": file_id,
                        "filename": file_filename,
                        "size": file_size
                    }
                    self._client.enqueue(username=username, files=[file_payload])
                    print(f"[{song_query}] 📥 Enqueued!")
                    return {"username": username, "filename": file_filename}
                except Exception as e:
                    print(f"[{song_query}] ❌ Failed to enqueue: {e}")
                    continue
        return None
