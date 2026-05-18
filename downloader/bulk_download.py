import time
import os
import sys
from slskd_api import SlskdClient

# --- READ CONFIG FROM DOCKER ENVIRONMENT VARIABLES ---
SLSKD_HOST = os.environ.get("SLSKD_HOST", "http://localhost:5030")
SLSKD_API_KEY = os.environ.get("SLSKD_API_KEY", "none")
TEXT_FILE_PATH = "songs.txt"

# --- QUALITY FILTER CONFIG ---
TARGET_FORMATS = [".mp3", ".flac"]
TARGET_BITRATE = 320

# Initialize connection to slskd
client = SlskdClient(host=SLSKD_HOST, api_key=SLSKD_API_KEY)

def search_and_download(song_query):
    print(f"\n🔍 Searching for: '{song_query}'...")
    try:
        search_job = client.searches.search_text(song_query)
        search_id = search_job.get("id")
    except Exception as e:
        print(f"❌ Failed to create search for '{song_query}': {e}")
        return False

    print("⏳ Waiting 15 seconds for Soulseek to collect results...")
    time.sleep(15)
    
    try:
        responses = client.searches.search_responses(search_id)
    except Exception as e:
        print(f"❌ Failed to get results for '{song_query}': {e}")
        return False

    if not responses:
        print(f"⚠️ No results found for '{song_query}'")
        return False

    # Debug: print first file structure to check field names
    if responses and responses[0].get("files"):
        first_file = responses[0]["files"][0]
        print(f"  🔍 Debug - First file keys: {list(first_file.keys())}")
        print(f"  🔍 Debug - First file: {first_file}")

    # Iterate through search results
    for response in responses:
        username = response.get("username")
        files = response.get("files", [])
        
        for file in files:
            file_filename = file.get("filename", "")
            file_id = file.get("id")
            file_size = file.get("size", 0)
            file_bitrate = file.get("bitRate") or file.get("bitrate")

            file_ext = file_filename.lower().split(".")[-1]
            is_flac = file_ext == "flac"
            is_mp3_320 = file_ext == "mp3" and file_bitrate == TARGET_BITRATE

            # Debug: print file info to check response structure
            if file_ext in ["mp3", "flac"]:
                print(f"  📄 Found {file_ext.upper()}: {os.path.basename(file_filename)} | bitrate={file_bitrate}")

            # FILTER: Accept FLAC or MP3 320kbps
            if is_flac or is_mp3_320:
                print(f"✅ Found {file_ext.upper()} match: {os.path.basename(file_filename)} from user '{username}'")
                
                try:
                    file_payload = {
                        "id": file_id,
                        "filename": file_filename,
                        "size": file_size
                    }
                    
                    # Enqueue download
                    client.transfers.enqueue(username=username, files=[file_payload])
                    
                    print(f"📥 Successfully added to download queue!")
                    return True # Exit to move to next song in list
                except Exception as e:
                    print(f"❌ Failed to enqueue (trying next file): {e}")
                    continue

    print(f"❌ No FLAC or MP3 {TARGET_BITRATE}kbps file found for '{song_query}'.")
    return False

def main():
    if not os.path.exists(TEXT_FILE_PATH):
        print(f"❌ Error: File '{TEXT_FILE_PATH}' not found in container.")
        print(f"   Please create a 'songs.txt' file from 'songs.txt.example' and mount it into the container.")
        sys.exit(1)

    with open(TEXT_FILE_PATH, "r", encoding="utf-8") as f:
        songs = [line.strip() for line in f if line.strip()]

    print(f"📋 Loaded {len(songs)} songs from '{TEXT_FILE_PATH}'. Starting FLAC or MP3 320kbps scan...")

    successful = []
    failed = []

    for song in songs:
        if search_and_download(song):
            successful.append(song)
        else:
            failed.append(song)
        time.sleep(2) 

    # Print summary log
    print("\n" + "="*50)
    print("📊 DOWNLOAD SUMMARY")
    print("="*50)
    print(f"✅ Successfully enqueued ({len(successful)}):")
    for s in successful:
        print(f"{s}")
    print(f"\n❌ Failed to find/enqueue ({len(failed)}):")
    for f in failed:
        print(f"{f}")
    print("="*50)

    print("\n🎉 Scan complete! Check slskd Web UI at http://localhost:5030 to monitor download progress.")

if __name__ == "__main__":
    main()

