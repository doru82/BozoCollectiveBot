
from plistlib import loads

from dotenv import load_dotenv
import requests
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes



TOKEN: Final = '7762828730:AAG8Y-p6htv9Ud1uRXKON-477A1jnYcT5G4'
BOT_USERNAME: Final = "@BozoCollBot"
CHAT_ID: Final = '866672977269489677'
COLLECTION_SLUG: Final = 'bozo-collective'  # Ensure the slug is correct

MAGIC_EDEN_URL = f"https://api.magiceden.dev/v2/collections/{COLLECTION_SLUG}/stats"

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is BOZOOO! Starting to track Bozo Collective NFT sales!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bozos need no help :(")

async def bozo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("say it: BOZOS ARE BETTER!")

# Fetch sales data from Magic Eden API
async def fetch_sales_data():
    try:
        response = requests.get(MAGIC_EDEN_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching sales data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception occurred while fetching sales data: {e}")
        return None

# Track NFT sales and send updates
async def track_nft_sales(context: ContextTypes.DEFAULT_TYPE):
    sales_data = await fetch_sales_data()
    if sales_data:
        message = (
            f"🚀 Bozo Collective Sales Data:\n"
            f"🌟 Floor Price: {sales_data['floorPrice']} SOL\n"
            f"📈 Total Volume: {sales_data['totalVolume']} SOL\n"
            f"🕒 24h Sales: {sales_data['last24HoursSales']}\n"
            f"🔖 Total Listed: {sales_data['totalListed']}"
        )
        await context.bot.send_message(chat_id=CHAT_ID, text=message)

# Handle text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

# Handle errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused {context.error}')

# Response handler
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "hello" in processed:
        return "sup Bozo :)"
    if "how are you" in processed:
        return "STFU I'm good!"
    if "love bozos" in processed:
        return "U gAy"
    if "klarion" in processed:
        return "Our Nephew"

    return "say something smart BOZO!"

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('bozo', bozo_command))

    # Scheduler to track sales
    scheduler = AsyncIOScheduler()
    scheduler.add_job(track_nft_sales, 'interval', minutes=5, args=[app])
    scheduler.start()

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error
    app.add_error_handler(error)

    # Polls the bot
    print('Bot is running...')
    app.run_polling(poll_interval=5)








