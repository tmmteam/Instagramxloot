import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "7612230666:AAFQpNWHI-uba1Bs-e_2x5Bb4VHj41xsyHk")
GROUP_ID = int(os.getenv("GROUP_ID", "-1001801976314"))

LIKE_API = "https://instagram-like-nine.vercel.app/?url="
VIEW_API = "https://instagram-view-gilt.vercel.app/?url="

COOLDOWN_HOURS = 12
STORAGE_FILE = "storage.json"