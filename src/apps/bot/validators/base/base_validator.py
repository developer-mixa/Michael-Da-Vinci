from abc import ABC, abstractmethod
from aiogram.types import Message

class BaseTgValidator:

    def validate(self, message: Message) -> str:
        messageText = message.text
        self._do_validate(messageText)
        return messageText
    
    @abstractmethod
    def _do_validate(self, message: str) -> None:
        pass
