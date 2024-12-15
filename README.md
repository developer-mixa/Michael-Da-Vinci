Структура проекта

src -> основной код проекта
src/main -> часть, которая запускает бота, настраивает Webhook & Polling
src/core -> часть, в которой содержится всё то, что нужно для запуска проекта, а также некоторые общие утилиты

src/apps -> все приложения

src/apps/bot -> вся работа с ботом

src/apps/consumers -> все консюмеры, в каждом из них есть app.py запускающий консюмера

src/apps/common -> общие вещи, которые используются и ботом, и консюмером

Отмечу, что все консюмеры - ничего не знают о боте, и никак с ним не взаимодействуют напрямую 