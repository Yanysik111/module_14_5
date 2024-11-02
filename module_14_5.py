from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from crud_functions import *



connection = sqlite3.connect('prod.db')
cursor = connection.cursor()

connection = sqlite3.connect('users.db')
cursor = connection.cursor()
initiate_db()

#for i in range(1, 5):
     #cursor.execute("INSERT INTO Products (title, description, price) VALUES (?,?,?)",
                   #(f"Продукт_{i}", f"Описание_{i}", f"Цена_{100*i}"))

connection.commit()

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage= MemoryStorage())


kb = ReplyKeyboardMarkup()
but1 = KeyboardButton(text = 'Рассчитать')
but2 = KeyboardButton(text = 'Информация')
but3 = KeyboardButton(text = 'Купить')
but4 = KeyboardButton(text = 'Регистрация')
kb.add(but1, but2, but3, but4)
kb.resize_keyboard

ikb = InlineKeyboardMarkup()
ikb2 = InlineKeyboardMarkup()

butt1 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data='calories')
butt2 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data='formulas')
butt3 = InlineKeyboardButton(text = 'Product1', callback_data='product_buying')
butt4 = InlineKeyboardButton(text = 'Product2', callback_data='product_buying')
butt5 = InlineKeyboardButton(text = 'Product3', callback_data='product_buying')
butt6 = InlineKeyboardButton(text = 'Product4', callback_data='product_buying"')
ikb.add(butt1)
ikb.add(butt2)
ikb2.add(butt3)
ikb2.add(butt4)
ikb2.add(butt5)
ikb2.add(butt6)

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

users = get_all_products()

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит)')
    await RegistrationState.username.set()



@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    users_tabl =is_included(message.text)
    if users_tabl is False:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя:')
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer('Регистрация прошла успешно!')
    await state.finish()


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Тут будет информация о боте')

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = ikb)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open('files/1.png', 'rb') as img:
        await message.answer_photo(img, reply_markup=kb)
    await message.answer(f'Название: {users[0][0]} | Описание: {users[0][1]} | Цена: {users[0][2]} ')
    with open('files/2.png', 'rb') as img:
        await message.answer_photo(img, reply_markup=kb)
    await message.answer(f'Название: {users[1][0]} | Описание: {users[1][1]} | Цена: {users[1][2]} ')
    with open('files/3.png', 'rb') as img:
        await message.answer_photo(img, reply_markup=kb)
    await message.answer(f'Название: {users[2][0]} | Описание: {users[2][1]} | Цена: {users[2][2]} ')
    with open('files/4.png', 'rb') as img:
        await message.answer_photo(img, reply_markup=kb)
    await message.answer(f'Название: {users[3][0]} | Описание: {users[3][1]} | Цена: {users[3][2]} ')

    await message.answer('Выберите продукт для покупки: ', reply_markup=ikb2)

@dp.callback_query_handler(text = 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()
@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5', reply_markup = ikb)
    await call.answer()
@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = int(10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5)

    await message.answer(f'Ваша норма калорий: {result} ')
    await state.finish()

@dp.message_handler(commands = ['start'])
async def start(message):
    with open('files/privetstvie.png', 'rb') as img:
        await message.answer_photo(img,reply_markup = kb)
    await message.answer( 'Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler()
async def mes(message):
    await message.answer('Введите команду /start, чтобы начать общение.')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)