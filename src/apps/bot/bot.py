from aiogram import Bot, Dispatcher

bot: Bot
dp: Dispatcher


def setup_bot(bot_: Bot) -> None:
    global bot
    bot = bot_


def get_bot() -> Bot:
    global bot

    return bot


def setup_dp(dp_: Dispatcher) -> None:
    global dp
    dp = dp_


def get_dp() -> Dispatcher:
    global dp

    return dp
