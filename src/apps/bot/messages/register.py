from src.apps.bot.commands.commands import ACTIVATING

# success messages

ACCEPT_PRIVACY_POLICE = 'Продолжая, вы принимаете пользовательское соглашение и политику конфидициальности.'
SEND_LOCATION = 'Отправить мои координаты'
OK_TO_CONTINUE = 'Чтобы продолжить, значение должно быть "Ok"'
WHAT_YOUR_NAME = 'Как тебя зовут?'
HOW_OLD_YOU = 'Введите дату рождения в формате год-месяц-день (например, 2005-10-20)'
WHAT_YOUR_GENDER = 'Какой у тебя пол?'
ABOUT_YOU = 'Расскажи о себе'
WHERE_YOU_FROM = 'Из какого ты города?'
SEND_YOUR_PHOTO = 'Теперь пришли своё фото, его будут видеть другие пользователи'
PUSH_REGISTER_QUERY = 'Заявка отправлена в очередь на регистрацию, ожидайте...'
SUCCESS_REGISTER = f'Вы успешно зарегистрировались! Теперь вы можете показать профиль в ленте командой {ACTIVATING}'
ALREADY_REGISTER = 'Вы уже зарегистрированы!'
MUST_SEND_PHOTO = 'Отправьте фото'

# validation error messages

NAME_CAN_CONTAIN_LETTERS = 'Имя может содержать только буквы'
TOO_LONG_NAME = 'Не бывает такого длинного имени'
TOO_SHORT_NAME = 'Вас назвали буквой? Поправьте имя'
NAME_CANT_CONTAIN_SPACES = 'Имя не может содержать пробелы, уберите их'
NAME_BEGIN_CANT_BE_LOWER = 'Уважайте себя, напишите своё имя с большой буквы'
WRONG_GENDER = 'Леее, пол должен быть или "Парень", или "Девушка", третьего не дано'