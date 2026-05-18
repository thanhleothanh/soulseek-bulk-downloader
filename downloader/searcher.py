import os
from config import MAX_RETRIES, WAIT_TIMES, TARGET_BITRATE


class SongSearcher:
    def __init__(self, client):
        self._client = client

    def search(self, song_query):
        print(f"\n🔍 Searching for: '{song_query}'...")
        try:
            search_job = self._client.search_text(song_query)
            search_id = search_job.get("id")
        except Exception as e:
            print(f"❌ Failed to create search for '{song_query}': {e}")
            return None

        for attempt in range(MAX_RETRIES):
            wait_time = WAIT_TIMES[attempt]
            print(f"⏳ Attempt {attempt + 1}/{MAX_RETRIES} - Waiting {wait_time}s for Soulseek to collect results...")
            import time
            time.sleep(wait_time)

            try:
                responses = self._client.search_responses(search_id)
            except Exception as e:
                print(f"❌ Failed to get results for '{song_query}': {e}")
                continue

            if not responses:
                print(f"⚠️ No results found for '{song_query}' (Attempt {attempt + 1})")
                continue

            if attempt == 0 and responses and responses[0].get("files"):
                first_file = responses[0]["files"][0]
                print(f"  🔍 Debug - First file keys: {list(first_file.keys())}")
                print(f"  🔍 Debug - First file: {first_file}")

            result = self._find_matching_file(responses)
            if result:
                return result

        print(f"❌ No FLAC or MP3 {TARGET_BITRATE}kbps file found for '{song_query}' after {MAX_RETRIES} attempts.")
        return None

    def _find_matching_file(self, responses):
        for response in responses:
            username = response.get("username")
            files = response.get("files", [])

            for file in files:
                file_filename = file.get("filename", "")
                file_id = file.get("id")
                file_size = file.get("size", 0)
                file_bitrate = file.get("bitRate") or file.get("bitrate")

                file_ext = file_filename.lower().split(".")[-1]
                if not self._matches_quality(file_ext, file_bitrate):
                    continue

                if file_ext in ["mp3", "flac"]:
                    print(f"  📄 Found {file_ext.upper()}: {os.path.basename(file_filename)} | bitrate={file_bitrate}")

                print(f"✅ Found {file_ext.upper()} match: {os.path.basename(file_filename)} from user '{username}'")

                try:
                    file_payload = {
                        "id": file_id,
                        "filename": file_filename,
                        "size": file_size
                    }
                    self._client.enqueue(username=username, files=[file_payload])
                    print(f"📥 Successfully added to download queue!")
                    return {"username": username, "filename": file_filename}
                except Exception as e:
                    print(f"❌ Failed to enqueue (trying next file): {e}")
                    continue
        return None

    def _matches_quality(self, file_ext, file_bitrate):
        if file_ext == "flac":
            return True
        if file_ext == "mp3" and file_bitrate == TARGET_BITRATE:
            return True
        return False
