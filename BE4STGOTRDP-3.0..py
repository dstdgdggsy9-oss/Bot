# ^𝐁 ᴇ 𝐀 s 𝐓 ~ 💗...!!?_bot_multi.py
import asyncio
import json
import os
import random
import time
import telegram.error
from datetime import datetime, timedelta, timezone
from telegram import Update, InputSticker, Sticker
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging
import yt_dlp
from gtts import gTTS
import requests
import io

# ---------------------------
# CONFIG
# ---------------------------
TOKENS = [
"8512037996:AAF6Fq9hysEdRuRoY60qoxzwsX2NxLIcTLA",
"8374417622:AAHHfCUWsK38QEhBR7u1yN0phZ7RInnu6ps",
"8342137992:AAEpWeUjXLzDWZmPX2ISWE7o5NzcsbGmt5Q",
"8571518744:AAFh2qvUhxwjFcY-FPvZ4L9t3SJ8wWgwdGg"
]

CHAT_ID = 7697311496
OWNER_ID = 8160881443
SUDO_FILE = "8160881443"
STICKER_FILE = "stickers.json"
VOICE_CLONES_FILE = "voice_clones.json"
tempest_API_KEY = "sk_e326b337242b09b451e8f18041fd0a7149cc895648e36538"

# ---------------------------
# tempest VOICE CHARACTERS
# ---------------------------
VOICE_CHARACTERS = {
    1: {"name": "Urokodaki", "voice_id": "VR6AewLTigWG4xSOukaG", "description": "Deep Indian voice", "style": "deep_masculine"},
    2: {"name": "Kanae", "voice_id": "EXAVITQu4vr4xnSDxMaL", "description": "Cute sweet voice", "style": "soft_feminine"},
    3: {"name": "Uppermoon", "voice_id": "AZnzlk1XvdvUeBnXmlld", "description": "Creepy dark deep voice", "style": "dark_creepy"},
    4: {"name": "Tanjiro", "voice_id": "VR6AewLTigWG4xSOukaG", "description": "Heroic determined voice", "style": "heroic"},
    5: {"name": "Nezuko", "voice_id": "EXAVITQu4vr4xnSDxMaL", "description": "Cute mute sounds", "style": "cute_mute"},
    6: {"name": "Zenitsu", "voice_id": "AZnzlk1XvdvUeBnXmlld", "description": "Scared whiny voice", "style": "scared_whiny"},
    7: {"name": "Inosuke", "voice_id": "VR6AewLTigWG4xSOukaG", "description": "Wild aggressive voice", "style": "wild_aggressive"},
    8: {"name": "Muzan", "voice_id": "AZnzlk1XvdvUeBnXmlld", "description": "Evil mastermind voice", "style": "evil_calm"},
    9: {"name": "Shinobu", "voice_id": "EXAVITQu4vr4xnSDxMaL", "description": "Gentle but deadly voice", "style": "gentle_deadly"},
    10: {"name": "Giyu", "voice_id": "VR6AewLTigWG4xSOukaG", "description": "Silent serious voice", "style": "silent_serious"}
}

# ---------------------------
# RAID TEXTS & EMOJIS
# ---------------------------
RAID_TEXTS = ["×~🌷GAY🌷×~","~×🌼BITCH🌼×~","~×🌻LESBIAN🌻×~","~×🌺CHAPRI🌺×~","~×🌹TMKC🌹×~","~×🏵️TMR🏵×~️","~×🪷TMKB🪷×~","~×💮CHUS💮×~","~×🌸HAKLE🌸×~","~×🌷GAREEB🌷×~","~×🌼RANDY🌼×~","~×🌻POOR🌻×~","~×🌺TATTI🌺×~","~×🌹CHOR🌹×~","~×🏵️CHAMAR🏵️×~","~×🪷SPERM COLLECTOR🪷×~","~×💮CHUTI LULLI💮×~","~×🌸KALWA🌸×~","~×🌷CHUD🌷×~","~×🌼CHUTKHOR🌼×~","~×🌻BAUNA🌻×~","~×🌺MOTE🌺×~","~×🌹GHIN ARHA TUJHSE🌹×~","~×🏵️CHI POOR🏵×~️","~🪷PANTY CHOR🪷~","~×💮LAND CHUS💮×~","~×🌸MUH MAI LEGA🌸×~","~×🌷GAND MARE 🌷×~","~×🌼MOCHI WALE 🌼×~","~×🌻GANDMARE 🌻×~","~×🌺KIDDE 🌺×~","~×🌹LAMO 🌹×~","~×🏵️BIHARI 🏵×~️","~×🪷MULLE 🪷×~","~×💮NAJAYESH LADKE 💮×~","~×🌸GULAM 🌸×~","~×🌷CHAMCHA🌷×~","~×🌼EWW 🌼×~","~×🌻CHOTE TATTE 🌻×~","~×🌺SEX WORKER 🌺×~","~×🌹CHINNAR MA KE LADKE 🌹×~"]
exonc_TEXTS = ["×🌼×","×🌻×","×🪻×","×🏵️×","×💮×","×🌸×","×🪷×","×🌷×","×🌺×","×🥀×","×🌹×","×💐×","×💋×","×❤️‍🔥×","×❤️‍🩹×","×❣️×","×♥️×","×💟×","×💌×","×💕×","×💞×","×💓×","×💗×","×💖×","×💝×","×💘×","×🩷×","×🤍×","×🩶×","×🖤×","🤎×","×💜×","×💜×","×🩵×","×💛×","×🧡×","×❤️×"]
NCEMO_EMOJIS = ["😀","😃","😄","😁","😆","😅","😂","🤣","😭","😉","😗","😗","😚","😘","🥰","😍","🤩","🥳","🫠","🙃","🙂","🥲","🥹","😊","☺️","😌","😏","🤤","😋","😛","😝","😜","🤪","🥴","😔","🥺","😬","😑","😐","😶","😶‍🌫️","🫥","🤐","🫡","🤔","🤫","🫢","🤭","🥱","🤗","🫣","😱","🤨","🧐","😒","🙄","😮‍💨","😤","😠","😡","🤬","😞","😓","😟","😥","😢","☹️","🙁","🫤","😕","😰","😨","😧","😦","😮","😯","😲","😳","🤯","😖","😣","😩","😵","😵‍💫","🫨","🥶","🥵","🤢","🤮","😴","😪","🤧","🤒","🤕","😷","😇","🤠","🤑","🤓","😎","🥸"]
ANI_EMOJIS = ["🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼","🐨","🐯","🦁","🐮","🐷","🐸","🐵","🐔","🐧","🐦","🐤","🐣","🦅","🦆","🦢","🦉","🐴","🦄","🐝","🪱","🐛","🦋","🐌","🐞","🐜","🦟","🦗","🕷","🕸","🦂","🐢","🐍","🦎","🦖","🦕","🐙","🦑","🦐","🦞","🦀","🐡","🐠","🐟","🐬","🐳","🐋","🦈","🐊","🐅","🐆","🦓","🦍","🦧","🐘","🦛","🦏","🐪","🐫","🦒","🦘","🦬","🐃","🐄","🐎","🐖","🐏","🐑","🐐","🦌","🐕","🐩","🦮","🐈","🐕‍🦺","🐓","🦃","🦚","🦜","🦢","🦩","🕊","🐇","🦝","🦨","🦡","🦦","🦥","🐁","🐀","🐿","🦔"]
FLAG_EMOJIS = ["🏁","🚩","🎌","🏴","🏳️","🇦🇫","🇦🇱","🇩🇿","🇦🇸","🇦🇩","🇦🇴","🇦🇮","🇦🇶","🇦🇬","🇦🇷","🇦🇲","🇦🇼","🇦🇺","🇦🇹","🇦🇿","🇧🇸","🇧🇭","🇧🇩","🇧🇧","🇧🇾","🇧🇪","🇧🇿","🇧🇯","🇧🇲","🇧🇹","🇧🇴","🇧🇦","🇧🇼","🇧🇷","🇮🇴","🇻🇬","🇧🇳","🇧🇬","🇧🇫","🇧🇮","🇰🇭","🇨🇲","🇨🇦","🇮🇨","🇨🇻","🇧🇶","🇰🇾","🇨🇫","🇹🇩","🇨🇱","🇨🇳","🇨🇽","🇨🇨","🇨🇴","🇰🇲","🇨🇬","🇨🇩","🇨🇰","🇨🇷","🇨🇮","🇭🇷","🇨🇺","🇨🇼","🇨🇾","🇨🇿","🇩🇰","🇩🇯","🇩🇲","🇩🇴","🇪🇨","🇪🇬","🇸🇻","🇬🇶","🇪🇷","🇪🇪","🇪🇹","🇪🇺","🇫🇰","🇫🇴","🇫🇯","🇫🇮","🇫🇷","🇬🇫","🇵🇫","🇹🇫","🇬🇦","🇬🇲","🇬🇪","🇩🇪","🇬🇭","🇬🇮","🇬🇷","🇬🇱","🇬🇩","🇬🇵","🇬🇺","🇬🇹","🇬🇬","🇬🇳","🇬🇼","🇬🇾","🇭🇹","🇭🇳","🇭🇰","🇭🇺","🇮🇸","🇮🇳","🇮🇩","🇮🇷","🇮🇶","🇮🇪","🇮🇲","🇮🇱","🇮🇹","🇯🇲","🇯🇵","🇯🇪","🇯🇴","🇰🇿","🇰🇪","🇰🇮","🇽🇰","🇰🇼","🇰🇬","🇱🇦","🇱🇻","🇱🇧","🇱🇸","🇱🇷","🇱🇾","🇱🇮","🇱🇹","🇱🇺","🇲🇴","🇲🇰","🇲🇬","🇲🇼","🇲🇾","🇲🇻","🇲🇱","🇲🇹","🇲🇭","🇲🇶","🇲🇷","🇲🇺","🇾🇹","🇲🇽","🇫🇲","🇲🇩","🇲🇨","🇲🇳","🇲🇪","🇲🇸","🇲🇦","🇲🇿","🇲🇲","🇳🇦","🇳🇷","🇳🇵","🇳🇱","🇳🇨","🇳🇿","🇳🇮","🇳🇪","🇳🇬","🇳🇺","🇳🇫","🇰🇵","🇲🇵","🇳🇴","🇴🇲","🇵🇰","🇵🇼","🇵🇸","🇵🇦","🇵🇬","🇵🇾","🇵🇪","🇵🇭","🇵🇳","🇵🇱","🇵🇹","🇵🇷","🇶🇦","🇷🇪","🇷🇴","🇷🇺","🇷🇼","🇼🇸","🇸🇲","🇸🇹","🇸🇦","🇸🇳","🇷🇸","🇸🇨","🇸🇱","🇸🇬","🇸🇽","🇸🇰","🇸🇮","🇬🇸","🇸🇧","🇸🇴","🇿🇦","🇰🇷","🇸🇸","🇪🇸","🇱🇰","🇧🇱","🇸🇭","🇰🇳","🇱🇨","🇵🇲","🇻🇨","🇸🇩","🇸🇷","🇸🇿","🇸🇪","🇨🇭","🇸🇾","🇹🇼","🇹🇯","🇹🇿","🇹🇭","🇹🇱","🇹🇬","🇹🇰","🇹🇴","🇹🇹","🇹🇳","🇹🇷","🇹🇲","🇹🇨","🇹🇻","🇻🇮","🇺🇬","🇺🇦","🇦🇪","🇬🇧","🇺🇸","🇺🇾","🇺🇿","🇻🇺","🇻🇦","🇻🇪","🇻🇳","🇼🇫","🇪🇭","🇾🇪","🇿🇲","🇿🇼"]
HEART_EMOJIS = ["❤️","🧡","💛","💚","💙","💜","🖤","🤍","🤎","💔","❣️","💕","💞","💓","💗","💖","💘","💝","💟","❤️‍🔥","❤️‍🩹","🏩","💒","💌"]
KISS_EMOJIS = ["😘","😗","😚","😙","💋","👄","💏","👩‍❤️‍💋‍👨","👨‍❤️‍💋‍👨","👩‍❤️‍💋‍👩","🫦","💌","💘","💝"]
MOON_EMOJIS = ["🌑","🌒","🌓","🌔","🌕","🌖","🌗","🌘","🌙","🌚","🌛","🌜","☀️","🌝","🌕"]

# ---------------------------
# GLOBAL STATE
# ---------------------------
if os.path.exists(SUDO_FILE):
    try:
        with open(SUDO_FILE, "r") as f:
            _loaded = json.load(f)
            SUDO_USERS = set(int(x) for x in _loaded)
    except: SUDO_USERS = {OWNER_ID}
else: SUDO_USERS = {OWNER_ID}

group_tasks, spam_tasks, react_tasks, exonc_tasks, photo_tasks = {}, {}, {}, {}, {}
active_reactions, chat_photos = {}, {}
slide_targets, slidespam_targets = set(), set()
apps, bots = [], []
delay, spam_delay, exonc_delay, GLOBAL_DELAY = 0.1, 0.5, 0.05, 0.5
sticker_mode = True

logging.basicConfig(level=logging.INFO)

# ---------------------------
# CORE FUNCTIONS
# ---------------------------
def only_sudo(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if uid == OWNER_ID or uid in SUDO_USERS: return await func(update, context)
        # UPDATED MESSAGE BELOW
        await update.message.reply_text("𝐘ᴏᴜʀ 𝐖ᴏʀᴅs 𝐀ʀᴇ 𝐖ᴏʀᴅʟᴇss 𝐈 𝐎ɴʟʏ 𝐒ᴇʀ𝐯ᴇ 𝐌ᴏɴᴀʀᴄʜ\n^𝐁 ᴇ 𝐀 s 𝐓 ~ 💗...!!?")
    return wrapper

async def bot_loop(bot, chat_id, base, mode):
    i = 0
    while True:
        try:
            text = f"{base} {RAID_TEXTS[i % len(RAID_TEXTS)]}" if mode == "gcnc" else f"{NCEMO_EMOJIS[i%len(NCEMO_EMOJIS)]} {base}"
            await bot.set_chat_title(chat_id, text)
            i += 1
            await asyncio.sleep(max(0.5, delay))
        except: await asyncio.sleep(1.0)

# ---------------------------
# COMMAND HANDLERS
# ---------------------------
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🪷^𝐁 ᴇ 𝐀 s 𝐓 ~ 💗...!!? TG NC— Commands 🪷\nUse -help")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "<b>^𝐁 ᴇ 𝐀 s 𝐓 ~ 💗...!!? 𝐕𝟏𝟎 𝐁𝐄𝐓</b>\n\n✦ 𝐍𝐂: -gcnc -ncemo -nctime -raidnc\n✦ 𝐄𝐌𝐎𝐉𝐈: -ncemoani -ncemoflag\n✦ 𝐒𝐏𝐄𝐄𝐃: -ncbaap -betanc -ultragc\n✦ 𝐒𝐏𝐀𝐌: -spam -unspam\n✦ 𝐒𝐋𝐈𝐃𝐄: -targetslide -slidespam"
    await update.message.reply_text(help_text, parse_mode="HTML")

@only_sudo
async def raidnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ Usage: -raidnc <name>")
    prefix = " ".join(context.args)
    chat_id = update.message.chat_id
    if chat_id in group_tasks: [t.cancel() for t in group_tasks[chat_id]]
    group_tasks[chat_id] = [asyncio.create_task(bot_loop(b, chat_id, prefix, "gcnc")) for b in bots]
    await update.message.reply_text(f"🔥 RAID NC STARTED: {prefix}")

@only_sudo
async def stopall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for d in [group_tasks, spam_tasks, exonc_tasks]:
        for ts in d.values(): [t.cancel() for t in ts]
        d.clear()
    await update.message.reply_text("⏹ ALL ACTIVITIES STOPPED!")

# ---------------------------
# SYSTEM STARTUP (PASSWORD REMOVED)
# ---------------------------
def build_app(token):
    from telegram.ext import PrefixHandler
    app = Application.builder().token(token).build()
    app.add_handler(PrefixHandler("-", "start", start_cmd))
    app.add_handler(PrefixHandler("-", "help", help_cmd))
    app.add_handler(PrefixHandler("-", "raidnc", raidnc))
    app.add_handler(PrefixHandler("-", "stopall", stopall))
    return app

async def run_all_bots():
    unique_tokens = list(set(t.strip() for t in TOKENS if t.strip()))
    for token in unique_tokens:
        try:
            app = build_app(token)
            apps.append(app); bots.append(app.bot)
            await app.initialize(); await app.start()
            await app.updater.start_polling()
            print(f"🚀 Bot started: {token[:10]}...")
        except Exception as e: print(f"❌ Failed: {e}")
    
    print(f"🎉 ^𝐁 ᴇ 𝐀 s 𝐓 ~ 💗...!!? V10 Beta Ultra Multi is running with {len(bots)} bots!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    print("\n✅ INITIALIZING ^𝐁 ᴇ 𝐀 s 𝐓 ~ 💗...!!? SYSTEM...")
    try:
        asyncio.run(run_all_bots())
    except KeyboardInterrupt:
        print("\n🛑 ^𝐁 ᴇ 𝐀 s 𝐓 ~ 💗...!!? V10 Beta Shutting Down...")
