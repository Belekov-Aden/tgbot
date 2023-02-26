from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def inlineKeyboardsApps(name: str, ikb: InlineKeyboardMarkup):
    ikb.add(InlineKeyboardButton(text='{name}'.format(name=name), callback_data='name_app'+name))


async def inlineKeyboardsAppsDelete(name: str, ikb: InlineKeyboardMarkup):
    ikb.add(InlineKeyboardButton(text='{name}'.format(name=name), callback_data='app_delete'+name))