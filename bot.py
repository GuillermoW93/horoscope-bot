import os
import requests
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Add logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define functions to fetch daily, weekly, monthly horoscopes
def fetch_horoscope(sign, period="daily"):
    try:
        API_URL = f"https://horoscope-app-api.vercel.app/api/v1/get-horoscope/{period}?sign={sign.lower()}"
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("horoscope_data", "No horoscope available.")
        else:
            return f"Failed to fetch {period} horoscope."
    except requests.exceptions.RequestException as e:
        return f"Error connecting to API, verify your API-token?: {str(e)}"

# Normalize zodiac sign input
def normalize_sign(sign):
    zodiac_signs = [
        "aries", "taurus", "gemini", "cancer", "leo", "virgo",
        "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
    ]
    sign = sign.strip().lower()
    if sign in zodiac_signs:
        return sign.capitalize()
    else:
        return None

# Here we greet the user
def welcome(update, context):
    update.message.reply_text(
        "🌟 Welcome to the Horoscope Bot! 🌟\n\n"
        "✨ Unlock daily, weekly, and monthly horoscopes tailored to your zodiac sign. 🌟\n\n"
        "Available Commands:\n\n"
        "🗓️ /daily   <zodiac_sign> - Discover your daily horoscope.\n"
        "📅 /weekly  <zodiac_sign> - Get insights for the week ahead.\n"
        "📆 /monthly <zodiac_sign> - See what the stars predict for the month.\n\n"
        "Example:\n"
        "📖 Try `/daily Aries` to get started!\n\n"
        "💫 Let the stars guide you every day!"
    )

# Daily horoscope command
def daily(update, context):
    if not context.args:
        update.message.reply_text("Please provide a zodiac sign. Example: /daily Aries.")
        return

    sign = normalize_sign(' '.join(context.args))
    if not sign:
        update.message.reply_text("Invalid zodiac sign. Please provide a valid one (e.g., Aries, Taurus, etc.).")
        return

    logger.info(f"Fetching daily horoscope for sign: {sign}")
    horoscope_message = fetch_horoscope(sign, period="daily")
    update.message.reply_text(f"♈ {sign} (Daily):\n{horoscope_message}")

# Weekly horoscope command
def weekly(update, context):
    if not context.args:
        update.message.reply_text("Please provide a zodiac sign. Example: /weekly Aries.")
        return

    sign = normalize_sign(' '.join(context.args))
    if not sign:
        update.message.reply_text("Invalid zodiac sign. Please provide a valid one (e.g., Aries, Taurus, etc.).")
        return

    logger.info(f"Fetching weekly horoscope for sign: {sign}")
    horoscope_message = fetch_horoscope(sign, period="weekly")
    update.message.reply_text(f"♈ {sign} (Weekly):\n{horoscope_message}")

# Monthly horoscope command
def monthly(update, context):
    if not context.args:
        update.message.reply_text("Please provide a zodiac sign. Example: /monthly Aries.")
        return

    sign = normalize_sign(' '.join(context.args))
    if not sign:
        update.message.reply_text("Invalid zodiac sign. Please provide a valid one (e.g., Aries, Taurus, etc.).")
        return

    logger.info(f"Fetching monthly horoscope for sign: {sign}")
    horoscope_message = fetch_horoscope(sign, period="monthly")
    update.message.reply_text(f"♈ {sign} (Monthly):\n{horoscope_message}")

# Main function of the bot
def main():
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    if not telegram_token:
        raise ValueError("Telegram token not found. Set it as an environment variable.")
    
    updater = Updater(telegram_token, use_context=True)
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))  # Welcome new users
    dp.add_handler(CommandHandler("welcome", welcome))
    dp.add_handler(CommandHandler("daily", daily))
    dp.add_handler(CommandHandler("weekly", weekly))
    dp.add_handler(CommandHandler("monthly", monthly))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()