from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F
from .router import router


@router.message(F.text == "rear")
async def test(message: Message):
    print("wtf1")
    await message.answer('ура')
    print("wtf2")