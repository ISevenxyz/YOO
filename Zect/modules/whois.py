from datetime import datetime

from pyrogram import filters
from pyrogram.types import User, InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.raw import functions
from pyrogram.errors import PeerIdInvalid
from Zect import app
from config import PREFIX


def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id


infotext = (
    "**[{full_name}](tg://user?id={user_id})**\n"
    " > UserID: `{user_id}`\n"
    " > First Name: `{first_name}`\n"
    " > Last Name: `{last_name}`\n"
    " > Username: `{username}`\n"
)


def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


@app.on_message(filters.command("whois", PREFIX) & filters.me)
async def whois(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await message.reply("I don't know that User.")
        return
    desc = await client.get_chat(get_user)
    desc = desc.description
    await message.edit_text(
        infotext.format(
            full_name=FullName(user),
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name or "",
            username=user.username or ""
        ),
        disable_web_page_preview=True,
    )


@app.on_message(filters.command("id", PREFIX) & filters.me)
async def id(client, message):
    cmd = message.command
    chat_id = message.chat.id
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await message.edit("I don't know that User.")
        return
    text = "**User ID**: `{}`\n**Chat ID**: `{}`".format(user.id, chat_id)
    await message.edit(text)