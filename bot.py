from aiogram import types, executor,Bot,Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext


from my_buttons import main_menu

from datas import add_to_db,show_autos


api = '7724991152:AAHq4ijEZlItcrmsgLLPgpv6DK3zDbra7fY'
bot = Bot(api)
storage = MemoryStorage()
dp  =Dispatcher(bot,storage=storage)

class AddCarState(StatesGroup):
    marka = State()
    color = State()
    year = State()
    price = State()
    photo = State()



@dp.message_handler(commands=['start'])
async def send_hi(sms:types.Message):
    await sms.answer('Asslamu aleykum',
                     reply_markup=main_menu)

@dp.message_handler(text='Add Car')
async def send_car_reg(sms:types.Message):
    await sms.answer('OOO jana mashina')
    await sms.answer('Bizge mashinanin markasin jazin:')
    await AddCarState.marka.set()

@dp.message_handler(state=AddCarState.marka)
async def send_marka(sms:types.Message,state:FSMContext):
    async with state.proxy() as car:
        car['marka']=sms.text#car={'marka':'Cobalt'}
    await sms.answer('Al endi renin jaz:')
    await AddCarState.color.set()



@dp.message_handler(state=AddCarState.color)
async def send_marka(sms:types.Message,state:FSMContext):
    async with state.proxy() as car:
        car['color']=sms.text#car={'marka':'Cobalt'}

    await sms.answer('Al endi jilin jaz:')
    await AddCarState.year.set()

@dp.message_handler(state=AddCarState.year)
async def send_marka(sms:types.Message,state:FSMContext):
    async with state.proxy() as car:
        car['year']=sms.text#car={'marka':'Cobalt'}
    await sms.answer('Al endi cenasin jaz:')
    await AddCarState.price.set()

@dp.message_handler(state=AddCarState.price)
async def send_marka(sms:types.Message,state:FSMContext):
    async with state.proxy() as car:
        car['price']=sms.text#car={'marka':'Cobalt'}
    await sms.answer('Al endi cenasin jaz:')
    await AddCarState.photo.set()

@dp.message_handler(state=AddCarState.photo,content_types='photo')
async def send_marka(sms:types.Message,state:FSMContext,):
    async with state.proxy() as car:
        car['photo']=sms.photo[0]['file_id']#car={'marka':'Cobalt'}
    await sms.answer('Siz mashinani qostiniz:')
    await sms.answer_photo(
        photo=car['photo'],
        caption=f'''
markasi :{car['marka']},
reni:{car['color']}
'''
    )
    await add_to_db(marka=car['marka'],
                    color=car['color'],
                    price=car['price'],
                    year=car['year'],
                    photo=car['photo']
                    )
    await state.finish()


@dp.message_handler(text='Buy Car')
async def send_cars(sms:types.Message):
    cars = await show_autos()
    for i in cars:
        await sms.answer_photo(
            photo=i[-1],
            caption=f'''{i[0]},
{i[1]},
{i[2]},
{i[3]}
''')

if __name__=='__main__':
    executor.start_polling(dp,skip_updates=True)