# telegram-calendar
![car](https://github.com/mikaelangelm/telegram-calendar-public/blob/main/documents/avatar.png?raw=true)

## Используется:
* (СДЕЛАНО) Flask
* [heroku/logs](https://dashboard.heroku.com/apps/telethon-calendar/logs)
* (СДЕЛАНО) [Google API Calendar](https://developers.google.com/calendar/api/v3/reference?apix=true) ([credentials](https://console.cloud.google.com/apis/credentials?project=calendar-312707))
* (НЕ ДЕЛАТЬ) api положения транспорта ЕКБ [1) 2GIS](https://catalog.api.2gis.ru/doc/2.0/transport/), [2) 4PDA app](https://4pda.to/forum/index.php?showtopic=829759&st=20#entry108915388)
* (СДЕЛАНО) [Будить](https://youtu.be/jC55EM-PP6Q?t=546) сервер каждые 25 мин при помощи [uptimerobot](https://uptimerobot.com/dashboard#mainDashboard)
* 20211104 алгоритм перенесен с вебхуков боту на питон телеграм-клиент (telebot -> telethon)

## Алгоритм:
* Инициализировать telethon ([1](https://my.telegram.org/auth?to=apps), [2](https://colab.research.google.com/drive/1e8DJFEwurgLnZ__0eFZgt91Ms4a3VDsk#scrollTo=IkzgtOV8NkN0&line=14&uniqifier=1))
* [Репозиторий](https://github.com/mikaelangelm/transport-ekb/) формируется на основании Docker-подобных требований [Dyno configuration](https://devcenter.heroku.com/articles/dynos#dyno-configurations) и [instr. for Prepare&Deploy APP](https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true#prepare-the-app)
* [Deploy](https://dashboard.heroku.com/apps/transport-ekb/deploy/github)&[Overview](https://dashboard.heroku.com/apps/transport-ekb/resources): deploy and configure Dynos

## Функционал python:
* обработка вебхука|нового сообщения TG c отправкой обезличенных данных о свободном времени на "сегодня", "завтра", "сегодня HH:mm" согласно Google Calendar
* (планируется) автоотправка времени/расстояния автобуса до остановки "Новомосковская" согласно положению транспорта ЕКБ, при скором наступлении события Google Calendar

## Статьи:
- [https://www.bustime.ru/about/](https://github.com/norn/bustime/blob/master/api/views.py)
- [Как я сделал свой «Яндекс.Транспорт» с расписанием и автобусами](https://habr.com/ru/company/dataart/blog/411249/)
- [MarkedText — маркдаун здорового человека](https://habr.com/ru/post/536448/)
- [Мега-Учебник Flask, Часть 18: Развертывание на Heroku Cloud](https://habr.com/ru/post/237517/)
- [telethon на heroku](https://vc.ru/dev/158757-sozdanie-i-razvertyvanie-retranslyatora-telegram-kanalov-ispolzuya-python-i-heroku)
