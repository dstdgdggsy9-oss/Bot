# ^𝐁 ᴇ 𝐀 s 𝐓 ~ 💗...!!?_bot_multi.py
import asyncio
import json
import os
import random
import time
import logging
import telegram.error
from telegram import Update
from telegram.ext import Application, ContextTypes, PrefixHandler, Defaults
from telegram.request import HTTPXRequest

# ---------------------------
# CONFIG
# ---------------------------
TOKENS = [
    "8512037996:AAF6Fq9hysEdRuRoY60qoxzwsX2NxLIcTLA",
    "8374417622:AAHHfCUWsK38QEhBR7u1yN0phZ7RInnu6ps",
    "8342137992:AAEpWeUjXLzDWZmPX2ISWE7o5NzcsbGmt5Q",
    "8571518744:AAFh2qvUhxwjFcY-FPvZ4L9t3SJ8wWgwdGg"
]

OWNER_ID = 8160881443
SUDO_USERS = {OWNER_ID} # Faster than file I/O on GitHub

# ---------------------------
# DATA ASSETS
# ---------------------------
RAID_TEXTS = ["×~🌷GAY🌷×~","~×🌼BITCH🌼×~","~×🌻LESBIAN🌻×~","~×🌺CHAPRI🌺×~","~×🌹TMKC🌹×~","~×🏵️TMR🏵×~️","~×🪷TMKB🪷×~","~×💮CHUS💮×~","~×🌸HAKLE🌸×~","~×🌷GAREEB🌷×~","~×🌼RANDY🌼×~","~×🌻POOR🌻×~","~×🌺TATTI🌺×~","~×🌹CHOR🌹×~","~×🏵️CHAMAR🏵️×~","~×🪷SPERM COLLECTOR🪷×~","~×💮CHUTI LULLI💮×~","~×🌸KALWA🌸×~","~×🌷CHUD🌷×~","~×🌼CHUTKHOR🌼×~"]
NCEMO_EMOJIS = ["😀","😃","😄","😁","😆","😅","😂","🤣","😭","😉","😗","😘","🥰","😍"]
ANI_EMOJIS = ["🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼","🐨","🐯","🦁","🐮","🐷","🐸"]
FLAG_EMOJIS = ["🏁","🚩","🎌","🏴","🏳️","🇦🇫","🇦🇱","🇩🇿","🇦🇸","🇦🇩","🇦🇴","🇦🇮"]

group_tasks = {}
spam_tasks = {}
apps, bots = [], []
GLOBAL_DELAY = 0.05 

logging.basicConfig(level=logging.ERROR)

def only_sudo(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user and update.effective_user.id in SUDO_USERS:
            return await func(update, context)
    return wrapper

async def nc_loop(bot, chat_id, base, mode):
    i = 0
    while True:
        try:
            if mode == "raidnc": text = f"{base} {RAID_TEXTS[i % len(RAID_TEXTS)]}"
            elif mode == "ncemo": text = f"{NCEMO_EMOJIS[i % len(NCEMO_EMOJIS)]} {base}"
            elif mode == "nctime": text = f"⌚ {time.strftime('%H:%M:%S')} | {base}"
            elif mode == "ncemoani": text = f"{ANI_EMOJIS[i % len(ANI_EMOJIS)]} {base}"
            elif mode == "ncemoflag": text = f"{FLAG_EMOJIS[i % len(FLAG_EMOJIS)]} {base}"
            else: text = f"🔥 {base} 🔥"
            
            asyncio.create_task(bot.set_chat_title(chat_id=chat_id, title=text))
            i += 1
            await asyncio.sleep(GLOBAL_DELAY)
        except telegram.error.RetryAfter as e: await asyncio.sleep(e.retry_after)
        except Exception: await asyncio.sleep(0.5)

async def spam_loop(bot, chat_id, text):
    while True:
        try:
            tasks = [bot.send_message(chat_id=chat_id, text=text, disable_web_page_preview=True) for _ in range(5)]
            await asyncio.gather(*tasks, return_exceptions=True)
            await asyncio.sleep(GLOBAL_DELAY)
        except telegram.error.RetryAfter as e: await asyncio.sleep(e.retry_after)
        except Exception: break

@only_sudo
async def start_nc_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text.split()[0][1:] 
    if not context.args: return
    prefix, chat_id = " ".join(context.args), update.message.chat_id
    if chat_id in group_tasks:
        for t in group_tasks[chat_id]: t.cancel()
    group_tasks[chat_id] = [asyncio.create_task(nc_loop(b, chat_id, prefix, cmd)) for b in bots]
    await update.message.reply_text(f"🚀 {cmd.upper()} ON GITHUB RUNNER!")

@only_sudo
async def spam_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return
    text, chat_id = " ".join(context.args), update.message.chat_id
    spam_tasks[chat_id] = [asyncio.create_task(spam_loop(b, chat_id, text)) for b in bots]
    await update.message.reply_text("🌪 GITHUB BURST SPAM!")

@only_sudo
async def stop_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    for d in [group_tasks, spam_tasks]:
        if cid in d:
            for t in d[cid]: t.cancel()
            del d[cid]
    await update.message.reply_text("⏹ STOPPED.")

def build_app(token):
    # Reduced pool size for GitHub environment stability
    t_request = HTTPXRequest(connection_pool_size=20, read_timeout=5, write_timeout=5)
    app = Application.builder().token(token).request(t_request).defaults(Defaults(block=False)).build()
    all_cmds = ["gcnc", "ncemo", "nctime", "raidnc", "ncemoani", "ncemoflag", "ncbaap", "betanc", "ultragc"]
    for c in all_cmds: app.add_handler(PrefixHandler("-", c, start_nc_task))
    app.add_handler(PrefixHandler("-", "spam", spam_handler))
    app.add_handler(PrefixHandler("-", "unspam", stop_all))
    app.add_handler(PrefixHandler("-", "stopall", stop_all))
    return app

async def run_all_bots():
    # Use Gather for bot initialization to avoid sequential delay
    init_tasks = []
    for token in list(set(TOKENS)):
        token = token.strip()
        if not token: continue
        app = build_app(token)
        apps.append(app); bots.append(app.bot)
        init_tasks.append(app.initialize())
        init_tasks.append(app.start())
        # Disable signal handlers as GitHub Actions doesn't allow standard signal management in child threads
        init_tasks.append(app.updater.start_polling(drop_pending_updates=True, stop_signals=None))
    
    await asyncio.gather(*init_tasks)
    print("👑 ^𝐁 ᴇ 𝐀 s 𝐓 ~ GITHUB MODE ONLINE")
    while True: await asyncio.sleep(3600) # Prevents workflow exit

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_all_bots())
    except KeyboardInterrupt:
        pass
        
