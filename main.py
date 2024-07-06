import asyncio, os
from pyrogram import *
from pyrogram.types import *
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from database.mongo import *
from config import *
from data import *

dz = Client(
    "genids_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=token
)

@dz.on_message(filters.command ("start") & filters.private)
async def start(dz, m):
    me = m.from_user.id
    chat = m.chat.id
    if not await cek(me):
        try:
            await tambah(me)
        except:
            pass
    await m.reply_text(start_txt.format(me, chat))

@dz.on_message(filters.command ("id"))
async def id_cmd(dz, m):
    if m.reply_to_message:
        rep = m.reply_to_message.from_user.id
        msgt = m.reply_to_message.id
        chat = m.chat.id
        me = m.from_user.id
        await m.reply_text(reply_txt.format(rep, msgt, chat, me))
    else:
        me = m.from_user.id
        chat = m.chat.id
        await m.reply_text(start_txt.format(me, chat))

@dz.on_message(filters.forwarded & filters.private)
async def fw_cmd(dz, m):
    if m.forward_from:
        chat_id = m.forward_from.id
        me = m.from_user.id
        msgt = m.forward_from_message_id
        dc_id = m.forward_from.dc_id
        await m.reply_text(fw1_txt.format(chat_id, me, msgt, dc_id))
    elif m.forward_from_chat:
        title = m.forward_from_chat.title 
        chat_id = m.forward_from_chat.id
        me = m.from_user.id
        msgt = m.forward_from_message_id
        dc_id = m.forward_from_chat.dc_id
        await m.reply_text(fw2_txt.format(title, chat_id, me, msgt, dc_id))
    else:
        await m.reply_text(hide_txt)
        
# BROADCAST CMD
@dz.on_message(filters.command('users') & filters.user(1814359323))
async def get_users(dz, m):
    msg = await dz.send_message(chat_id=m.chat.id, text="Processing...")
    users = await semua()
    await msg.edit(f"{len(users)} users are using this bot")

@dz.on_message(filters.command('broadcast') & filters.user(1814359323))
async def send_text(dz, m):
    if m.reply_to_message:
        query = await semua()
        broadcast_msg = m.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await m.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await hapus(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await hapus(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await m.reply("<b>Reply message to use broadcast command👮🏻‍♂️</b>")
        await asyncio.sleep(8)
        await msg.delete()
    
dz.run(print("RUNING..."))
print("STOP")