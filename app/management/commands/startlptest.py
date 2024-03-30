from django.core.management.base import BaseCommand
from app.bot.vk.client import Client
import asyncio

class Command(BaseCommand):
    help = 'Start VkBot'

    def handle(self, *args, **options):
        asyncio.run(self.start_vk_bot())

    async def start_vk_bot(self):
        client = Client()
        try:
            while True:
                events = await client.listen()
                for event in events:
                    print(event)  # Обработка события
                    
        except KeyboardInterrupt:
            print("Остановлено пользователем")
        finally:
            await client.session.close()  # Асинхронное закрытие сессии при выходе

