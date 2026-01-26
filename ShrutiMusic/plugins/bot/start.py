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
from ShrutiMusic.utils.inline import help_pannel_page1, start_panel
from config import BANNED_USERS
from strings import get_string


DEVELOPER_NAME = "nox_shadowx"
BOT_USERNAME = "ChikooMusic_bot"

SUPPORT_GROUP = "https://t.me/Music_Brigade_Chatting_zone"
SUPPORT_CHANNEL = "https://t.me/BrokenXworld"
DEVELOPER_CONTACT = "https://t.me/nox_shadowx"

ADD_TO_GROUP_URL = f"https://t.me/{BOT_USERNAME}?startgroup=true"


def main_start_buttons(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("➕ Add Me To Group", url=ADD_TO_GROUP_URL),
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


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    buttons = main_start_buttons(_)

    # /start with args
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        # /start help
        if name[0:4] == "help":
            keyboard = help_pannel_page1(_)
            return await message.reply_text(
                text=_["help_1"].format(SUPPORT_GROUP)
                + f"\n\n<b>Developer:</b> <code>{DEVELOPER_NAME}</code>",
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )

        # /start sudolist
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=(
                        f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n"
                        f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                        f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}\n\n"
                        f"<b>Developer:</b> <code>{DEVELOPER_NAME}</code>"
                    ),
                )
            return

        # /start info_<ytid>
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"

            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]

            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )

            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text="👥 Support Group", url=SUPPORT_GROUP),
                    ],
                    [
                        InlineKeyboardButton("➕ Add Me To Group", url=ADD_TO_GROUP_URL),
                        InlineKeyboardButton("📢 Support Channel", url=SUPPORT_CHANNEL),
                    ],
                    [
                        InlineKeyboardButton("👤 Developer Contact", url=DEVELOPER_CONTACT),
                    ],
                ]
            )

            await m.delete()

            # send thumbnail photo (safe URL)
            try:
                await app.send_photo(
                    chat_id=message.chat.id,
                    photo=thumbnail,
                    caption=searched_text + f"\n\n<b>Developer:</b> <code>{DEVELOPER_NAME}</code>",
                    reply_markup=key,
                )
            except:
                await message.reply_text(
                    searched_text + f"\n\n<b>Developer:</b> <code>{DEVELOPER_NAME}</code>",
                    reply_markup=key,
                    disable_web_page_preview=True,
                )

            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOG_GROUP_ID,
                    text=(
                        f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n"
                        f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                        f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}\n\n"
                        f"<b>Developer:</b> <code>{DEVELOPER_NAME}</code>"
                    ),
                )
            return

        # /start start
        if name == "start":
            UP, CPU, RAM, DISK = await bot_sys_stats()
            return await message.reply_text(
                text=_["start_2"].format(
                    message.from_user.mention, app.mention, UP, DISK, CPU, RAM
                )
                + f"\n\n<b>Developer:</b> <code>{DEVELOPER_NAME}</code>",
                reply_markup=buttons,
                disable_web_page_preview=True,
            )

    # Normal /start
    UP, CPU, RAM, DISK = await bot_sys_stats()

    await message.reply_text(
        text=_["start_2"].format(
            message.from_user.mention, app.mention, UP, DISK, CPU, RAM
        )
        + f"\n\n<b>Developer:</b> <code>{DEVELOPER_NAME}</code>",
        reply_markup=buttons,
        disable_web_page_preview=True,
    )

    if await is_on_off(2):
        return await app.send_message(
            chat_id=config.LOG_GROUP_ID,
            text=(
                f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n"
                f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}\n\n"
                f"<b>Developer:</b> <code>{DEVELOPER_NAME}</code>"
            ),
        )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)

    group_buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("➕ Add Me To Group", url=ADD_TO_GROUP_URL),
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

    await message.reply_text(
        text=_["start_1"].format(app.mention, get_readable_time(uptime))
        + f"\n\n<b>Developer:</b> <code>{DEVELOPER_NAME}</code>",
        reply_markup=group_buttons,
        disable_web_page_preview=True,
    )
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            SUPPORT_GROUP,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)

                await message.reply_text(
                    text=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    )
                    + f"\n\n<b>Developer:</b> <code>{DEVELOPER_NAME}</code>",
                    reply_markup=InlineKeyboardMarkup(out),
                    disable_web_page_preview=True,
                )

                await add_served_chat(message.chat.id)
                await message.stop_propagation()

        except Exception as ex:
            print(ex)
