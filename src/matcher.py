DEFAULT_FORMAT_PRIORITY = ["flac", "m4a", "mp3", "ogg"]
DEFAULT_BITRATE_PREFERENCE = [320, 256, 192, 128]


class FileMatcher:
    def find_best(self, responses):
        for fmt in DEFAULT_FORMAT_PRIORITY:
            if fmt == "mp3":
                match = self._search_by_bitrate_ladder(responses)
            else:
                match = self._find_first(responses, lambda ext, br: ext == fmt)
            if match:
                return match
        return None

    @staticmethod
    def _search_by_bitrate_ladder(responses):
        for br in DEFAULT_BITRATE_PREFERENCE:
            match = FileMatcher._find_first(responses, lambda ext, b: ext == "mp3" and b == br)
            if match:
                return match
        return None

    @staticmethod
    def _find_first(responses, predicate):
        for response in responses:
            username = response.get("username")
            for file in response.get("files", []):
                ext = file.get("filename", "").lower().split(".")[-1]
                bitrate = file.get("bitRate") or file.get("bitrate")
                if predicate(ext, bitrate):
                    return username, file
        return None
