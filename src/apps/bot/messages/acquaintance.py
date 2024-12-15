from src.apps.bot.commands.commands import ACTIVATING
from src.apps.bot.emoji.emojies import STOP, LIKE, DISLIKE


STOP_SEARCHING = 'Поиск остановлен...'
ACQUAINTANCE_REQUIREMENTS = f'Ответ должен использовать один из символов: {LIKE},{DISLIKE},{STOP}'
NOT_REGISTERED = 'Вы не зарегестрированы!'
NO_USERS_FOUND = 'К сожалению, не найдено ни одного пользователя =('
PROFILE_MUST_BE_ACTIVATED = f'Для поиска, нужно активировать профиль командой {ACTIVATING}'
SOMETHING_WENT_WRONG = 'Что-то пошло не так... Попробуйте ещё раз или обратитесь к разработчику'
USER_INFO_TEMPLATE = '{name}, {age} \n\n{description}'
MUTUALL_LIKE_TEMPLATE = 'Вау! Ваша симпатия оказалась взаимной! 🤩👫 \n\nТеперь вы можете продолжить разговор прямо здесь @{username}'