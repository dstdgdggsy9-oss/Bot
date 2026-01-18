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
SUDO_USERS = {OWNER_ID}

# ---------------------------
# DATA ASSETS
# ---------------------------
RAID_TEXTS = ["×~🌷GAY🌷×~","~×🌼BITCH🌼×~","~×🌻LESBIAN🌻×~","~×🌺CHAPRI🌺×~","~×🌹TMKC🌹×~","~×🏵️TMR🏵×~️","~×🪷TMKB🪷×~","~×💮CHUS💮×~","~×🌸HAKLE🌸×~","~×🌷GAREEB🌷×~"]
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
        await update.message.reply_text("𝐘ᴏᴜʀ 𝐖ᴏʀᴅs 𝐀ʀᴇ 𝐖ᴏʀᴅʟᴇss")
    return wrapper

# ---------------------------
# CORE LOOPS
# ---------------------------
async def nc_loop(bot, chat_id, base, mode):
    i = 0
    while True:
        try:
            if mode == "raidnc": text = f"{base} {RAID_TEXTS[i % len(RAID_TEXTS)]}"
            elif mode == "ncemo": text = f"{NCEMO_EMOJIS[i % len(NCEMO_EMOJIS)]} {base}"
            elif mode in ["ultragc", "ncbaap", "betanc"]: text = f"🚀 {base} 🚀 {random.choice(NCEMO_EMOJIS)}"
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

# ---------------------------
# HANDLERS
# ---------------------------
@only_sudo
async def ping_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    msg = await update.message.reply_text("🚀 Pinging...")
    end_time = time.time()
    ms = round((end_time - start_time) * 1000, 2)
    await msg.edit_text(f"🚀 **𝐏𝐎𝐍𝐆!**\n🛰 **Latency:** `{ms}ms`\n🤖 **Bots Active:** `{len(bots)}`")

@only_sudo
async def start_nc_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text.split()[0][1:] 
    if not context.args: return
    prefix, chat_id = " ".join(context.args), update.message.chat_id
    if chat_id in group_tasks:
        for t in group_tasks[chat_id]: t.cancel()
    group_tasks[chat_id] = [asyncio.create_task(nc_loop(b, chat_id, prefix, cmd)) for b in bots]
    await update.message.reply_text(f"⚡ {cmd.upper()} ACTIVATED!")

@only_sudo
async def spam_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return
    text, chat_id = " ".join(context.args), update.message.chat_id
    spam_tasks[chat_id] = [asyncio.create_task(spam_loop(b, chat_id, text)) for b in bots]
    await update.message.reply_text("🌪 ULTRA BURST SPAM ON!")

@only_sudo
async def stop_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    for d in [group_tasks, spam_tasks]:
        if cid in d:
            for t in d[cid]: t.cancel()
            del d[cid]
    await update.message.reply_text("⏹ ALL KILLED.")

# ---------------------------
# SYSTEM BOOT
# ---------------------------
def build_app(token):
    t_request = HTTPXRequest(connection_pool_size=100, read_timeout=1, write_timeout=1)
    app = Application.builder().token(token).request(t_request).defaults(Defaults(block=False)).build()
    
    all_cmds = ["gcnc", "ncemo", "nctime", "raidnc", "ncemoani", "ncemoflag", "ncbaap", "betanc", "ultragc"]
    for c in all_cmds: app.add_handler(PrefixHandler("-", c, start_nc_task))
    app.add_handler(PrefixHandler("-", "ping", ping_handler))
    app.add_handler(PrefixHandler("-", "spam", spam_handler))
    app.add_handler(PrefixHandler("-", "unspam", stop_all))
    app.add_handler(PrefixHandler("-", "stopall", stop_all))
    return app

async def run_all_bots():
    for token in list(set(TOKENS)):
        token = token.strip()
        if not token: continue
        try:
            app = build_app(token)
            apps.append(app); bots.append(app.bot)
            await app.initialize()
            await app.start()
            await app.updater.start_polling(drop_pending_updates=True)
        except Exception: pass
    
    print("👑 ^𝐁 ᴇ 𝐀 s 𝐓 ~ ULTRA ENGINE RUNNING")
    while True: await asyncio
        

