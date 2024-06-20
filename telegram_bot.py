import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import json

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Trading bot's API token
TOKEN = 'Bot-token'
BOT_USERNAME = '###TradeWithPumpBot'

# Defining the commands and their descriptions
commands = {
    'start': 'Start interacting with the bot.',
    'help': 'Show help information.',
    'invite': 'Get an invite link to share the bot.',
    'send': 'Send a custom message to the user/group',
    'commands': 'List all available commands.'
}

# Loading chat IDs from file
try:
    with open('chat_ids.json', 'r') as f:
        chat_ids = set(json.load(f))#storing chatids for future use cases
except FileNotFoundError:
    chat_ids = set()

async def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    chat_id = update.message.chat_id
    chat_ids.add(chat_id)
    logger.info(f"Added chat ID: {chat_id}")
    await update.message.reply_text('Hi! I am your Trading bot.')

async def help_command(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    await update.message.reply_text('Hi! I am your Trading bot. Use /commands to see all available commands.')

async def log_chat_id(update: Update, context: CallbackContext):
    """Log the chat ID of the incoming message."""
    chat_id = update.message.chat_id
    chat_ids.add(chat_id)
    logger.info(f"Chat ID: {chat_id}")
    await update.message.reply_text(f"Chat ID: {chat_id} has been logged.")
    
async def invite_link(update: Update, context: CallbackContext):
    """Send the bot invite link to the groups."""
    logger.info("Received /invite command")
    invite_link = f'https://t.me/{BOT_USERNAME}'
    await update.message.reply_text(f'Invite your friends to use this bot: {invite_link}')
    
async def list_commands(update: Update, context: CallbackContext):
    """List all available commands."""
    logger.info("Received /commands command")
    commands_list = "\n".join([f"/{cmd} - {desc}" for cmd, desc in commands.items()])
    await update.message.reply_text(f"Available commands:\n{commands_list}")

async def send_message(update: Update, context: CallbackContext):
    """Send a message to all stored chat IDs."""
    text = 'This is a test message from the bot.'
    for chat_id in chat_ids:
        try:
            await context.bot.send_message(chat_id=chat_id, text=text)
            logger.info(f"Message sent to {chat_id}")
        except Exception as e:
            logger.error(f"Failed to send message to {chat_id}: {e}")

# Save chat IDs to file
def save_chat_ids():
    with open('chat_ids.json', 'w') as f:
        json.dump(list(chat_ids), f)

def main():
    """Start the bot."""
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("send", send_message))
    application.add_handler(CommandHandler("invite", invite_link))
    application.add_handler(CommandHandler("commands",list_commands))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_chat_id))

    application.run_polling()
    save_chat_ids()

if __name__ == '__main__':
    main()
