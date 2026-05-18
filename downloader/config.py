import os

SLSKD_HOST = os.environ.get("SLSKD_HOST", "http://localhost:5030")
SLSKD_API_KEY = os.environ.get("SLSKD_API_KEY", "none")
TEXT_FILE_PATH = "songs.txt"

TARGET_FORMATS = [".mp3", ".flac"]
TARGET_BITRATE = 320

MAX_WORKERS = 10
MAX_RETRIES = 3
WAIT_TIMES = [15, 25, 35]
TRANSFER_CHECK_DELAY = 5

SUCCESS_STATES = {"Queued", "InProgress", "Complete", "Initializing"}
