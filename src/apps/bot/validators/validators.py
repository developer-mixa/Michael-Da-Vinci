import re

from .errors import ValidationError
from .base.base_validator import BaseTgValidator

MAX_NAME_LEN = 15
MIN_NAME_LEN = 2

class NameValidator(BaseTgValidator):
    def _do_validate(self, message: str):
        if not message.isalpha():
            raise ValidationError('Имя может содержать только буквы')
        if len(message) >= MAX_NAME_LEN:
            raise ValidationError('Не бывает такого длинного имени')
        if len(message) < MIN_NAME_LEN:
            raise ValidationError('Вас назвали буквой? Поправьте имя')
        if message.count(' ') > 0 or message.count('\n') > 0:
            raise ValidationError('Имя не может содержать пробелы, уберите их')
        if message[0].islower():
            raise ValidationError(f'Уважайте себя, напишите своё имя с большой буквы - {message.title()}')


class AgeValidator(BaseTgValidator):
    def _do_validate(self, message: str):
        if not message.isdigit():
            raise ValidationError('Возраст должен быть числом')
        if int(message) < 0:
            raise ValidationError('Вы не можете быть настолько молодыми, число должно быть положительным')
        if int(message) >= 200:
            raise ValidationError('Леее, врятли вам 200+ лет')


class GenderValidator(BaseTgValidator):

    def _do_validate(self, message: str):
        if message != 'Парень' and message != 'Девушка':
            raise ValidationError('Леее, пол должен быть или "Парень", или "Девушка", третьего не дано')
