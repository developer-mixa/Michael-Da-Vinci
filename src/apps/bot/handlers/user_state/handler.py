import logging

from aiogram.types import Message

from .router import router
from aiogram import F

logger = logging.getLogger(__name__)

@router.message(F.text == '/activate')
def activate_profile(message: Message):
    pass

@router.message(F.text == '/deactivate')
def deactivate_profile(message: Message):
    pass
