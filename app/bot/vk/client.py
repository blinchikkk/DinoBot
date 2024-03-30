import aiohttp
from django.conf import settings
import json

class Client:
    def __init__(self):
        self.token = settings.VK_GROUP_ACCESS_TOKEN
        self.group_id = settings.VK_GROUP_ID
        self.api_version = settings.API_VERSION
        self.session = aiohttp.ClientSession()
        self.server = ''
        self.key = ''
        self.ts = ''

    async def call_to_api(self, method, params):
        """Запрос к VK API."""
        params['access_token'] = self.token
        params['v'] = self.api_version
        async with self.session.get(f'https://api.vk.com/method/{method}', params=params) as response:
            return await response.json()

    async def get_longpoll_server(self):
        """Получение параметров сервера Long Poll."""
        response = await self.call_to_api('groups.getLongPollServer', {'group_id': self.group_id})
        if response.get('response'):
            self.server = response['response']['server']
            self.key = response['response']['key']
            self.ts = response['response']['ts']
        else:
            print(response)

    async def listen(self):
        """Прослушивание событий с Long Poll сервера и возврат их."""
        if not self.server or not self.key:
            await self.get_longpoll_server()

        longpoll_url = f"{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25"
        async with self.session.get(longpoll_url) as response:
            data = await response.text()
            updates = json.loads(data)
            if 'ts' in updates:
                self.ts = updates['ts']
            
            return updates.get('updates', [])
