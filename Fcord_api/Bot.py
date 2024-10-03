import time
import asyncio
import httpx

from .data.errors import error_messages

class FcordBotStats:
    def __init__(self, bot, retry_after: int = 120, update_interval: int = 120):
        
        if retry_after <= 0:
            self.print("retry_after должно быть положительным числом. Сброшено до 120!")
            retry_after = 120
        if update_interval <= 0:
            self.print("update_interval должно быть положительным числом. Сброшено до 120!")
            update_interval = 120
        
        self.bot = bot
        self.base_url = f"https://mircord.xyz/api/monitoring/bots/{bot.user.id}/stats-update"
        self.headers = {'Authorization': bot.Fcord_api_key}
        self.retry_after = retry_after
        self.update_interval = update_interval
        self.last_request_time = 0
        self.running = False
        self.update_task = None

    def print(self, message: str) -> None:
        print(f"- [Fcord] - {message}")

    async def activate(self, update_interval: int = None) -> None:
        if update_interval:
            self.update_interval = update_interval
        if not self.running:
            self.running = True
            self.update_task = asyncio.create_task(self.run_update_loop())
            self.print(f"Асинхронная задача для обновления статистики запущена. Интервал обновления: {self.update_interval} секунд. Интервал повторной попытки при ошибке: {self.retry_after} секунд")

    async def stop(self) -> None:
        if self.running:
            self.running = False
            if self.update_task:
                self.update_task.cancel()
                try:
                    await self.update_task
                except asyncio.CancelledError:
                    self.print("Асинхронная задача для обновления статистики остановлена.")

    async def run_update_loop(self) -> None:
        while self.running:
            await self.send_stats()
            await asyncio.sleep(self.update_interval)

    async def send_stats(self) -> None:
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
                        self.print_mircord("Статистика успешно обновлена.")
                        self.last_request_time = time.time()
                    else:
                        await self.handle_error(response)

            except httpx.RequestError as e:
                self.print_mircord(f"Ошибка при отправке запроса: {e}")
            except Exception as e:
                self.print_mircord(f"Неизвестная ошибка: {e}")
        else:
            wait_time = 30 - (time.time() - self.last_request_time)
            self.print_mircord(f"Превышен лимит запросов. Подождите {wait_time:.2f} секунд.")

    async def handle_error(self, response: httpx.Response) -> None:
        status_code = response.status_code

        message = error_messages.get(status_code, f"Неожиданный код ошибки: {status_code}. Проверьте библиотеку.")
        self.print_mircord(f"Ошибка при отправке запроса: Код - {status_code} | {message}")

        if status_code == 429:
            await asyncio.sleep(self.retry_after)
            await self.send_stats()

    async def update_now(self) -> None:
        await self.send_stats()

    def get_time_since_last_update(self) -> str:
        elapsed_seconds = time.time() - self.last_request_time
        minutes, seconds = divmod(int(elapsed_seconds), 60)
        return f"{minutes} минут {seconds} секунд"

    def is_running(self) -> bool:
        return self.running

    async def update_interval(self, interval: int) -> None:
        self.update_interval = interval

    async def update_retry_after(self, retry_after: int) -> None:
        self.retry_after = retry_after
