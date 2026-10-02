from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup
from app.phrases import phrases
from SQL.db import init_db, add_task, get_tasks, delete_task, mark_done
import logging 
logger = logging.getLogger(__name__)
router = Router()
def build_task_keyboard(tasks):
    kb = []
    for t in tasks:
        rows = [types.InlineKeyboardButton(text="✅ Mark done", callback_data=f"done: {t[0]}"),
                (types.InlineKeyboardButton(text="🗑 Delete a task", callback_data=f"deleted: {t[0]}"))]
        kb.append(rows)
    return InlineKeyboardMarkup(inline_keyboard=kb) 
    

@router.message(Command("start"))
async def handle_message(message: types.Message):
        kb = types.ReplyKeyboardMarkup(
        keyboard=[[
            types.KeyboardButton(text="📋 My Tasks")
        ]],
    resize_keyboard=True
)
        await message.answer(phrases["/start"], reply_markup=kb)

@router.message(F.text == "📋 My Tasks")
async def handle_tasks(message: types.Message):
    results = get_tasks(message.from_user.id)
    if not results:
        await message.answer(phrases["empty_list"])
        return
    else:
        reply = ""
        for r in results:
            reply += f"Task:{r[2]}: {r[3]}\n"
    keyboard = build_task_keyboard(results)
    await message.answer(reply, reply_markup=keyboard)

@router.message(F.text)
async def handle_any_text(message: types.Message):
    add_task(message.from_user.id, message.text)
    await message.answer(phrases["add_task"])

@router.callback_query()
async def handle_two_texts(callback: types.CallbackQuery):
    parts = callback.data.split(":")
    task_id = int(parts[1])
    if parts[0] == "done":
        mark_done(task_id)
        await callback.answer(phrases["done"])
    elif parts[0] == "deleted":
        delete_task(task_id)
        await callback.answer(phrases["deleted"])
    results = get_tasks(callback.from_user.id)
    reply = ""
    for r in results:
        reply += f"Task:{r[2]}: {r[3]}\n"
    last_keyboard = build_task_keyboard(results)
    await callback.message.edit_text(reply, reply_markup=last_keyboard)
    await callback.answer()