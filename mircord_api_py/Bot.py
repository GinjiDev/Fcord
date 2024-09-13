import time
import asyncio
import httpx

class MircordBotStats:
    def __init__(self, bot, retry_after=120, update_interval=120):
        self.bot = bot
        self.base_url = "https://mircord.xyz/bot-stats"
        self.headers = {'Authorization': bot.mircord_api_key}
        self.retry_after = retry_after
        self.update_interval = update_interval
        self.last_request_time = 0
        self.running = False
        self.update_task = None

    async def activate(self, update_interval=None):
        if update_interval:
            self.update_interval = update_interval
        if not self.running:
            self.running = True
            self.update_task = asyncio.create_task(self.run_update_loop())
            print(f"[MIRCORD] Асинхронная задача для обновления статистики запущена. Интервал обновления: {self.update_interval} секунд. Интервал повторной попытки при ошибке: {self.retry_after} секунд")

    async def stop(self):
        if self.running:
            self.running = False
            if self.update_task:
                self.update_task.cancel()
                try:
                    await self.update_task
                except asyncio.CancelledError:
                    print("[MIRCORD] Асинхронная задача для обновления статистики остановлена.")

    async def run_update_loop(self):
        while self.running:
            await self.send_stats()
            await asyncio.sleep(self.update_interval)

    async def send_stats(self):
        server_count = len(self.bot.guilds)
        shards = self.bot.shard_count

        if self.last_request_time == 0 or (time.time() - self.last_request_time) >= 30:
            bot_stats = {
                'servers': server_count,
                'shards': shards
            }

            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(self.base_url, json=bot_stats, headers=self.headers)

                    if response.status_code == 200:
                        print("[MIRCORD] Статистика успешно обновлена.")
                        self.last_request_time = time.time()
                    else:
                        await self.handle_error(response)

            except httpx.RequestError as e:
                print(f"[MIRCORD] Ошибка при отправке запроса: {e}")
            except Exception as e:
                print(f"[MIRCORD] Неизвестная ошибка: {e}")
        else:
            wait_time = 30 - (time.time() - self.last_request_time)
            print(f"[MIRCORD] Превышен лимит запросов. Подождите {wait_time:.2f} секунд.")

    async def handle_error(self, response):
        status_code = response.status_code
        if status_code == 429:
            print("[MIRCORD] Ошибка: Превышен лимит запросов. Повтор через минуту.")
            await asyncio.sleep(self.retry_after)
            await self.send_stats()
        elif status_code in (401, 403):
            print("[MIRCORD] Ошибка: Неавторизован. Проверьте ваш API-ключ.")
        elif status_code == 404:
            print("[MIRCORD] Ошибка: Ресурс не найден. Проверьте URL.")
        elif status_code == 500:
            print("[MIRCORD] Ошибка на сервере. Попробуйте позже.")
        elif status_code == 502:
            print("[MIRCORD] Ошибка шлюза. Попробуйте позже.")
        elif status_code == 503:
            print("[MIRCORD] Сервис временно недоступен. Попробуйте позже.")
        elif status_code == 504:
            print("[MIRCORD] Тайм-аут шлюза. Попробуйте позже.")
        elif status_code == 302:
            print("[MIRCORD] Перенаправление: Запрашиваемый ресурс временно перемещен. Проверьте новый URL в заголовках ответа.")
        else:
            print(f"[MIRCORD] Ошибка при отправке запроса: Код - {status_code} | Возможно вы не обновили библиотеку или непредвиденный код.")

    async def update_now(self):
        await self.send_stats()
    
    def get_time_since_last_update(self):
        elapsed_seconds = time.time() - self.last_request_time
        minutes, seconds = divmod(int(elapsed_seconds), 60)
        return f"{minutes} минут {seconds} секунд"
    
    def is_running(self):
        return self.running
    
    async def update_interval(self, interval):
        self.update_interval = interval
        
    async def update_retry_after(self, retry_after):
        self.retry_after = retry_after