import os
from typing import Final
from telegram import Update
from telegram.ext import CommandHandler, Application, MessageHandler, ContextTypes, filters
from helper import get_today_timestamp
from summary import get_summary

BOT_TOKEN: Final = os.getenv('BOT_TOKEN')
BOT_USERNAME: Final = "@bugwhisperers_bot"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Help!')

async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:    
        resp = await get_summary()
        print(resp)

        ans = ''
        for data in resp:
            ans += f'User {data["name"]}:\n'
            ans += f'Daily Score: {data["daily_score"]}\n'
            ans += f'Weekly Score: {data["weekly_score"]}\n'
            ans += f'Monthly Score: {data["monthly_score"]}\n'
            ans += '............................................\n\n'
        await update.message.reply_text(ans)
    except Exception as e:
        print(e)
        await update.message.reply_text('Error!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type 
    text = update.message.text 

    if BOT_USERNAME in text and 'summary' in text.lower():
        await summary_command(update, context)
    else:
        return

if __name__ == '__main__':
    print('starting bot...')
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('summary', summary_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print('polling...')
    app.run_polling(poll_interval=5)