from general import get_full_text_general

from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from config import print_n_log, parse_markdown_v2, agent_rotation
from dotenv import load_dotenv
import os

load_dotenv()

async def summarize_everything(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        link = update.message.text

        if "http" not in link:
            raise Exception("Insert a valid link format. {} is not a valid link to summarize.".format(link))
        else:
            await update.message.reply_text(parse_markdown_v2("Working on This Article..."), parse_mode='markdownv2', reply_to_message_id=update.message.message_id)
            summaries = await get_full_text_general(url=link, user_agent=agent_rotation())
            for summary in summaries:
                summary = parse_markdown_v2(summary)
                if "1\. Key Points:" in summary:
                    summary = summary.replace("1\. Key Points:", "__*1️⃣ Key Points:*__\n")
                if "2\. Further Studies:" in summary:
                    summary = summary.replace("2\. Further Studies:", "__*2️⃣ Further Studies:*__\n")
                await update.message.reply_text(summary, parse_mode='markdownv2', reply_to_message_id=update.message.message_id)
    except Exception as e:
        await update.message.reply_text(parse_markdown_v2(str(e)), parse_mode='markdownv2', reply_to_message_id=update.message.message_id)

# Main function
def main():
    os.chdir(os.path.dirname(__file__))

    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.environ['TELEGRAM_BOT_TOKEN']).build()

    # on different commands - answer in Telegram
    application.add_handler(MessageHandler(filters.Text(), summarize_everything))

    # Start the Telegram server
    application.run_polling()

if __name__ == "__main__":
    main()