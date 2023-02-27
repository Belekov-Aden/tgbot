import messages
import asyncio


from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from main import dp
from aiogram.dispatcher.filters import Text, Filter
from functions import formatter_str
from sqilte import create_table, insert_id_users, insert_name_password, get_users_app, delete_app_from_db
from keyboards import inlineKeyboardsApps, inlineKeyboardsAppsDelete
from aiogram.types import ReplyKeyboardRemove


async def on_startapp(_):
    await create_table()


class UsersApp(StatesGroup):
    name = State()
    password = State()


@dp.message_handler(commands=['start'])
async def start_commands(message: types.Message) -> None:
    await insert_id_users(id_users=message.from_user.id)
    await message.answer(text=messages.MESSAGES['start'])


@dp.message_handler(commands=['help'])
async def help_commands(message: types.Message) -> None:
    await message.answer(text=messages.MESSAGES['help'])


@dp.message_handler(commands=['new_app'], state=None)
async def new_app_commands(message: types.Message) -> None:
    await message.answer(text=messages.MESSAGES['new_app_names'])

    await UsersApp.name.set()


@dp.message_handler(content_types=['text'],state=UsersApp.name)
async def users_set_name_app(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = await formatter_str(message.text)

    await message.answer(text=messages.MESSAGES['new_app_password'])
    await UsersApp.next()


@dp.message_handler(content_types=['text'],state=UsersApp.password)
async def users_set_name_app(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['password'] = await formatter_str(message.text)

    await insert_name_password(id=message.from_user.id, name=data['name'], password=data['password'])
    await state.finish()
    await message.answer(text=messages.MESSAGES['succesful'].format(data['name'], data['password']))


@dp.message_handler(commands=['my_apps'])
async def see_my_apps(message: types.Message) -> None:
    inlinekb = types.InlineKeyboardMarkup(row_width=4)
    for user in await get_users_app(id=message.from_user.id):
        await inlineKeyboardsApps(name=user.name, ikb=inlinekb)
    if len(inlinekb.inline_keyboard) == 0:
        await message.answer(text=messages.MESSAGES['empty_apps'])
    else:
        await message.answer(text=messages.MESSAGES['my_apps'],
                         reply_markup=inlinekb)


@dp.callback_query_handler(Text(startswith='name_app'))
async def get_password_from_bd(callback: types.CallbackQuery) -> None:
    for users in await get_users_app(id=callback.from_user.id):
        if callback.data == f'name_app{users.name}':
            msg = await callback.message.answer(text=users.password)
            await callback.answer()
            await asyncio.sleep(5)
            try:
                await msg.delete()
            except Exception:
                pass


@dp.message_handler(commands=['delete'])
async def delet_app_from_bd(message: types.Message) -> None:
    inlinekb = types.InlineKeyboardMarkup(row_width=4)
    for user in await get_users_app(id=message.from_user.id):
        await inlineKeyboardsAppsDelete(name=user.name, ikb=inlinekb)
    if len(inlinekb.inline_keyboard) == 0:
        await message.answer(text=messages.MESSAGES['empty_apps'])
    else:
        await message.answer(text=messages.MESSAGES['new_app_names'],
                         reply_markup=inlinekb)


@dp.callback_query_handler(Text(startswith='app_delete'))
async def delete_app_from_bd_cb(callback: types.CallbackQuery) -> None:
    for users in await get_users_app(id=callback.from_user.id):
        if callback.data == f'app_delete{users.name}':
            await delete_app_from_db(id=callback.from_user.id, name=users.name, password=users.password)
            inlinekb = types.InlineKeyboardMarkup(row_width=4)
            for user in await get_users_app(id=callback.from_user.id):
                await inlineKeyboardsAppsDelete(name=user.name, ikb=inlinekb)
            await callback.message.edit_reply_markup(reply_markup=inlinekb)

