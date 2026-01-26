import time

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from py_yt import VideosSearch

import config
from ShrutiMusic import app
from ShrutiMusic.misc import _boot_
from ShrutiMusic.plugins.sudo.sudoers import sudoers_list
from ShrutiMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from ShrutiMusic.utils import bot_sys_stats
from ShrutiMusic.utils.decorators.language import LanguageStart
from ShrutiMusic.utils.formatters import get_readable_time
from ShrutiMusic.utils.inline import help_pannel_page1
from config import BANNED_USERS
from strings import get_string


# ---------------------------
# YOUR CUSTOM LINKS / DETAILS
# ---------------------------
BOT_USERNAME = "ChikooMusic_bot"
SUPPORT_GROUP = "https://t.me/Music_Brigade_Chatting_zone"
SUPPORT_CHANNEL = "https://t.me/BrokenXworld"
DEVELOPER_CONTACT = "https://t.me/nox_shadowx"


# ---------------------------
# BUTTONS
# ---------------------------
def private_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➕ Add Me To Group",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton("👥 Support Group", url=SUPPORT_GROUP),
                InlineKeyboardButton("📢 Support Channel", url=SUPPORT_CHANNEL),
            ],
            [
                InlineKeyboardButton("👤 Developer Contact", url=DEVELOPER_CONTACT),
            ],
        ]
    )


def group_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("👥 Support Group", url=SUPPORT_GROUP),
                InlineKeyboardButton("📢 Support Channel", url=SUPPORT_CHANNEL),
            ],
            [
                InlineKeyboardButton("👤 Developer Contact", url=DEVELOPER_CONTACT),
            ],
        ]
    )


# ============================
# START COMMAND (PRIVATE)
# ============================
@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    # If user used /start with arguments
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        # -------- HELP --------
        if name[0:4] == "help":
            keyboard = help_pannel_page1(_)

            help_text = (
                "✨ **HELP MENU**\n\n"
                "Tap the buttons below to view commands & features.\n\n"
                f"👥 Support Group: {SUPPORT_GROUP}\n"
                f"📢 Support Channel: {SUPPORT_CHANNEL}\n"
                f"👤 Developer: {DEVELOPER_CONTACT}\n"
            )

            return await message.reply_text(
                help_text,
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )

        # -------- SUDO LIST --------
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=(
                        f"{message.from_user.mention} just started the bot to check <b>sudo list</b>.\n\n"
                        f"<b>User ID:</b> <code>{message.from_user.id}</code>\n"
                        f"<b>Username:</b> @{message.from_user.username}"
                    ),
                )
            return

        # -------- TRACK INFO --------
        if name[0:3] == "inf":
            m = await message.reply_text("🔎 Searching...")

            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)

            title = "Unknown"
            duration = "Unknown"
            views = "Unknown"
            thumbnail = None
            channellink = ""
            channel = "Unknown"
            link = ""
            published = "Unknown"

            for result in (await results.next())["result"]:
                title = result.get("title", "Unknown")
                duration = result.get("duration", "Unknown")
                views = result.get("viewCount", {}).get("short", "Unknown")
                thumbnail = result.get("thumbnails", [{}])[0].get("url", "")
                thumbnail = thumbnail.split("?")[0] if thumbnail else None
                channellink = result.get("channel", {}).get("link", "")
                channel = result.get("channel", {}).get("name", "Unknown")
                link = result.get("link", "")
                published = result.get("publishedTime", "Unknown")

            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )

            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link or SUPPORT_CHANNEL),
                        InlineKeyboardButton(text=_["S_B_9"], url=SUPPORT_GROUP),
                    ],
                ]
            )

            await m.delete()

            # Send thumbnail if available, else send text
            if thumbnail:
                try:
                    await app.send_photo(
                        chat_id=message.chat.id,
                        photo=thumbnail,
                        caption=searched_text,
                        reply_markup=key,
                    )
                except:
                    await message.reply_text(
                        searched_text,
                        reply_markup=key,
                        disable_web_page_preview=True,
                    )
            else:
                await message.reply_text(
                    searched_text,
                    reply_markup=key,
                    disable_web_page_preview=True,
                )

            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=(
                        f"{message.from_user.mention} just started the bot to check <b>track info</b>.\n\n"
                        f"<b>User ID:</b> <code>{message.from_user.id}</code>\n"
                        f"<b>Username:</b> @{message.from_user.username}"
                    ),
                )
            return

        # -------- /start start --------
        if name == "start":
            UP, CPU, RAM, DISK = await bot_sys_stats()

            start_text = (
                f"✨ HELLO {message.from_user.mention}\n\n"
                f"❖ WELCOME TO | @{BOT_USERNAME} |\n\n"
                "➤ A smart & elegant music bot built for Telegram voice chats.\n\n"
                "➤ Enjoy: Smooth Playback • HD Sound • No Lag\n\n"
                "➤ Sources: YouTube • Spotify • Apple • Saavn\n\n"
                "➤ Tap HELP to view all commands & features.\n\n"
                f"📌 Uptime: {UP}\n"
                f"💾 Disk: {DISK}\n"
                f"🧠 CPU: {CPU}\n"
                f"📌 RAM: {RAM}\n\n"
                "Developer: nox_shadowx"
            )

            await message.reply_text(
                start_text,
                reply_markup=private_buttons(),
                disable_web_page_preview=True,
            )

            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=(
                        f"{message.from_user.mention} just started the bot.\n\n"
                        f"<b>User ID:</b> <code>{message.from_user.id}</code>\n"
                        f"<b>Username:</b> @{message.from_user.username}"
                    ),
                )
            return

    # Normal /start
    UP, CPU, RAM, DISK = await bot_sys_stats()

    start_text = (
        f"✨ HELLO {message.from_user.mention}\n\n"
        f"❖ WELCOME TO | @{BOT_USERNAME} |\n\n"
        "➤ A smart & elegant music bot built for Telegram voice chats.\n\n"
        "➤ Enjoy: Smooth Playback • HD Sound • No Lag\n\n"
        "➤ Sources: YouTube • Spotify • Apple • Saavn\n\n"
        "➤ Tap HELP to view all commands & features.\n\n"
        f"📌 Uptime: {UP}\n"
        f"💾 Disk: {DISK}\n"
        f"🧠 CPU: {CPU}\n"
        f"📌 RAM: {RAM}\n\n"
        "Developer: nox_shadowx"
    )

    await message.reply_text(
        start_text,
        reply_markup=private_buttons(),
        disable_web_page_preview=True,
    )

    if await is_on_off(2):
        return await app.send_message(
            chat_id=config.LOG_GROUP_ID,
            text=(
                f"{message.from_user.mention} just started the bot.\n\n"
                f"<b>User ID:</b> <code>{message.from_user.id}</code>\n"
                f"<b>Username:</b> @{message.from_user.username}"
            ),
        )


# ============================
# START COMMAND (GROUP)
# ============================
@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    uptime = int(time.time() - _boot_)

    text = (
        f"🎵 {app.mention} is alive!\n\n"
        f"⏳ Uptime: {get_readable_time(uptime)}\n\n"
        f"👥 Support Group: {SUPPORT_GROUP}\n"
        f"📢 Support Channel: {SUPPORT_CHANNEL}\n\n"
        "Developer: nox_shadowx"
    )

    await message.reply_text(
        text,
        reply_markup=group_buttons(),
        disable_web_page_preview=True,
    )

    return await add_served_chat(message.chat.id)


# ============================
# WELCOME (BOT JOIN + NEW MEMBERS)
# ============================
@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            # Ban banned users
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
                continue

            # If bot joined
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                # Leave blacklisted chats
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{BOT_USERNAME}?start=sudolist",
                            SUPPORT_GROUP,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                welcome_text = (
                    f"🎧 {app.mention} has joined **{message.chat.title}**!\n\n"
                    "Thanks for adding me.\n"
                    "Use /start to see commands.\n\n"
                    f"👥 Support Group: {SUPPORT_GROUP}\n"
                    f"📢 Support Channel: {SUPPORT_CHANNEL}\n\n"
                    "Developer: nox_shadowx"
                )

                await message.reply_text(
                    welcome_text,
                    reply_markup=group_buttons(),
                    disable_web_page_preview=True,
                )

                await add_served_chat(message.chat.id)
                await message.stop_propagation()

            # If normal user joined
            else:
                try:
                    await message.reply_text(
                        f"👋 Welcome {member.mention} to **{message.chat.title}**!\n\n"
                        f"🎧 Powered by @{BOT_USERNAME}",
                        disable_web_page_preview=True,
                    )
                except:
                    pass

        except Exception as ex:
            print(ex)


# ============================
# VIDEO CHAT STARTED / ENDED
# ============================
@app.on_message(filters.video_chat_started, group=-1)
async def vc_started(_, message: Message):
    try:
        if await is_on_off(2):
            await app.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=f"🔴 <b>Video Chat Started</b>\n\n<b>Chat:</b> {message.chat.title}\n<b>ID:</b> <code>{message.chat.id}</code>",
            )
    except Exception as e:
        print(e)


@app.on_message(filters.video_chat_ended, group=-1)
async def vc_ended(_, message: Message):
    try:
        if await is_on_off(2):
            await app.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=f"⚫ <b>Video Chat Ended</b>\n\n<b>Chat:</b> {message.chat.title}\n<b>ID:</b> <code>{message.chat.id}</code>",
            )
    except Exception as e:
        print(e)
