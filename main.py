import os
from typing import Final
from telegram import Update
from telegram.ext import CommandHandler, Application, MessageHandler, ContextTypes, filters

from models import User
from utils import ahnaf_exists, mubasshir_exists, shafin_exists

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN: Final = os.getenv('BOT_TOKEN')
BOT_USERNAME: Final = os.getenv('BOT_USERNAME')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Help!')

async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = [
        User('Ahnaf.Shahriar.Asif', 'Ahnaf Shahriar Asif'),
        User('mub.ch', 'Mubasshir Chowdhury'),
        User('_blaNk_', 'Shafin Alam')
    ]
    try:    
        resp = []

        for user in users:
            
            resp.append(await user.get_summary())
        
        ans = ''

        resp.sort(key=lambda x: x['monthly_score'], reverse=True)

        for data in resp:
            ans += f'User {data["name"]}:\n'
            ans += f'Daily Score: {data["daily_score"]}\n'
            ans += f'Weekly Score: {data["weekly_score"]}\n'
            ans += f'Monthly Score: {data["monthly_score"]}\n'
            ans += '............................................\n\n'
        await update.message.reply_text(ans)

    except Exception as e:
        print(f'Error in the main file: {e}')
        await update.message.reply_text('Error!')

def status_str(user, submissions):
    ans = f'\n\nUser {user.name}:\n'
    ans += f'Number of accepted submissions: {len(submissions)}\n'
    cnt = 1
    for submission in submissions:
        ans += f'{cnt}. {submission["problem"]} (https://codeforces.com/contest/{submission["contest"]}/problem/{submission["problem_index"]})\n'
        cnt += 1
    ans += '....................................................\n\n'
    return ans

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type 
    text = update.message.text

    if (BOT_USERNAME in text or message_type == 'private' ) and 'summary' in text.lower():
        await summary_command(update, context)
    elif BOT_USERNAME in text or message_type == 'private':
        users = []
        
        if ahnaf_exists(text):
            users.append(User('Ahnaf.Shahriar.Asif', 'Ahnaf Shahriar Asif'))
        if mubasshir_exists(text):
            users.append(User('mub.ch', 'Mubasshir Chowdhury'))
        if shafin_exists(text):
            users.append(User('_blaNk_', 'Shafin Alam'))

        if len(users) == 0:
            return

        for user in users:
            await user.set_submissions()

        ans = ''

        if 'daily_status' in text.lower():
            for user in users:
                ans += status_str(user, user.daily_submissions)
            await update.message.reply_text(ans)
        elif 'weekly_status' in text.lower():
            for user in users:
                ans += status_str(user, user.weekly_submissions)
            await update.message.reply_text(ans)
        elif 'monthly_status' in text.lower():
            for user in users:
                ans += status_str(user, user.monthly_submissions)
            await update.message.reply_text(ans)
        else:
            return
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
    