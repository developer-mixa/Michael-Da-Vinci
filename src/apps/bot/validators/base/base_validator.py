from abc import abstractmethod

from aiogram.types import Message


class BaseTgValidator:

    def validate(self, message: Message) -> str:
        messageText = message.text
        if messageText is not None:
            self._do_validate(messageText)
            return messageText
        return ''

    @abstractmethod
    def _do_validate(self, message: str) -> None:
        pass
