import json
import os
import time
import logging
import requests
from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from config import TELEGRAM_TOKEN, GROUP_ID, LIKE_API, VIEW_API, COOLDOWN_HOURS, STORAGE_FILE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load / Save storage
def load_storage():
    if not os.path.exists(STORAGE_FILE):
        return {}
    with open(STORAGE_FILE, "r") as f:
        return json.load(f)

def save_storage(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f)

storage = load_storage()


def check_group(update: Update):
    return update.effective_chat.id == GROUP_ID


def format_time_remaining(ts):
    delta = timedelta(seconds=int(ts - time.time()))
    return str(delta)


def handle_claim(update: Update, context: CallbackContext, claim_type: str, api_url: str):
    user_id = str(update.effective_user.id)
    now = time.time()

    user_data = storage.get(user_id, {"like": 0, "view": 0})
    
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "WELCOME TO THE FAMILY OF AAYU\n\n"
        "GET UNLIMITED LIKES AND VIEWS\n\n"
        "GO TO @TMM_SUPPORT_CHAT\n"
        "AND CLAIM\n\n"
        "USE\n"
        "/Like {url}\n"
        "/View {url}\n\n"
        "@MOH_MAYA_OFFICIAL"
    )
    
    # Check if both claims used
    like_ok = now >= user_data.get("like", 0)
    view_ok = now >= user_data.get("view", 0)
    if not like_ok and not view_ok:
        update.message.reply_text("⏰ **Daily Limit Reached!**\n\nYou've used your free claim for today (2/2)", parse_mode="Markdown")
        return

    # Cooldown check for this type
    if now < user_data.get(claim_type, 0):
        remaining = format_time_remaining(user_data[claim_type])
        update.message.reply_text(f"Use after {remaining}")
        return

    # Require url
    if not context.args:
        update.message.reply_text(f"Usage: /{claim_type} <url>")
        return
    url = context.args[0]

    try:
        requests.get(api_url + url, timeout=30)
    except Exception as e:
        update.message.reply_text(f"API error: {e}")
        return

    # Update cooldown
    user_data[claim_type] = now + COOLDOWN_HOURS * 3600
    storage[user_id] = user_data
    save_storage(storage)

    if claim_type == "like":
        update.message.reply_text("LIKES SENT SUCCESSFULLY✅\n\nOrder will complete soon 🫶")
    else:
        update.message.reply_text("VIEWS SENT SUCCESSFULLY✅\n\nOrder will complete soon 🫶")


def like_command(update: Update, context: CallbackContext):
    if not check_group(update):
        return
    handle_claim(update, context, "like", LIKE_API)


def view_command(update: Update, context: CallbackContext):
    if not check_group(update):
        return
    handle_claim(update, context, "view", VIEW_API)


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("like", like_command))
    dp.add_handler(CommandHandler("view", view_command))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
