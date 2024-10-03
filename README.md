<p align="center">
    <!--<img class="logo" src="src/images/logo.png" alt="Mircord Logo" width="200">-->
</p>
<p align="center">
    <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
    <img src="https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white" alt="Discord">
    <img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</p>


# FCord_api.py

**FCord_api.py** — это Python-библиотека, предназначенная для интеграции с `discord.py`(+ с другими форками) и автоматического обновления статистики вашего бота на платформе [Fcord](https://mivian.ru/monitoring). Библиотека поддерживает асинхронные операции и включает механизм обработки ошибок, что обеспечивает стабильную работу и обновление статистики.

## Возможности

- **Асинхронные обновления**: Регулярное обновление статистики бота без блокировки других функций.
- **Гибкая настройка**: Возможность настройки интервалов обновления и логики повторных попыток при ошибках.
- **Обработка ошибок**: Логирование ошибок, таких как превышение лимитов запросов или проблемы с авторизацией, с понятными сообщениями.
- **Мониторинг в реальном времени**: Возможность отслеживания времени последнего обновления и статуса выполнения задачи обновления.

## Установка
Для работы FCord_api.py необходимы данные 2 библиотеки: `asyncio`, `httpx`.
Быстрая установка: `pip install git+https://github.com/GinjiDev/Fcord_API`
**для быстрой установки требуется наличие git**

Установите библиотеку путём загрузки архива -> перетащите папку **FCord_api** к своему проекту и импортируйте в вашем проекте:
```py
from Fcord_api.Bot import FcordBotStats
```

# Пример использования
## Инициализация
Для начала работы создайте экземпляр класса `FcordBotStats`, передав ему объект вашего бота и опциональные параметры для настройки интервалов обновления и повторных попыток:
```py
from Fcord_api.Bot import FcordBotStats

bot_stats = FcordBotStats(bot, retry_after=120, update_interval=120)
```

## Активация обновлений
Для запуска асинхронной задачи, которая будет обновлять статистику, вызовите метод `activate`:
```py
await bot_stats.activate()
```

## Остановка обновлений
Если вам нужно остановить обновления, используйте метод `stop`:
```py
await bot_stats.stop()
```

## Немедленное обновление
Для немедленного обновления статистики вызовите метод `update_now`:
```py
await bot_stats.update_now()
```

## Проверка статуса задачи обновления
Вы можете проверить, работает ли задача обновления, вызвав метод `is_running`:
```py
if bot_stats.is_running():
    print("Задача обновления запущена.")
else:
    print("Задача обновления остановлена.")
```

## Настройка интервалов
Вы можете настроить интервалы обновления и повторных попыток следующим образом:
```py
# Установить новый интервал обновления (в секундах)
await bot_stats.update_interval(60)

# Установить интервал повторных попыток при ошибке (в секундах)
await bot_stats.update_retry_after(90)
```

## Получение времени с момента последнего обновления
Чтобы узнать, сколько времени прошло с момента последнего успешного обновления статистики, используйте метод `get_time_since_last_update`:
```py
time_since_update = bot_stats.get_time_since_last_update()
print(f"Прошло времени с последнего обновления: {time_since_update}")
```

# Полный пример интеграции с discord.py
Ниже приведён полный пример использования библиотеки в боте, созданном на основе `discord.py`:
```py
import discord
from discord.ext import commands
from Fcord_api.Bot import FcordBotStats

intents = discord.Intents.default()
intents.guilds = True  # Необходимо для работы со списком серверов

# Создаём объект бота с использованием commands.Bot
bot = commands.Bot(command_prefix="!", intents=intents)
bot.Fcord_api_key = "MIRCORD_KEY"

# Событие, срабатывающее при запуске бота
@bot.event
async def on_ready():
    bot_stats = FcordBotStats(bot, retry_after=120, update_interval=120)
    await bot_stats.activate()  # Активация обновления статистики
    print(f"Бот {bot.user} запущен и Fcord_API_Py активен.")

# Запуск бота
bot.run('BOT-TOKEN')
```