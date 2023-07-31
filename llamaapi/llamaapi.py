import aiohttp
import asyncio
import requests
import nest_asyncio



class LlamaAPI:
    def __init__(self, api_token, hostname = 'https://api.llama-api.com', domain_path = '/chat/completions'):
        self.hostname = hostname
        self.domain_path = domain_path
        self.api_token = api_token
        self.headers = {'Authorization': f'Bearer {self.api_token}'}

        # Apply nest_asyncio to enable nested usage of asyncio's event loop
        nest_asyncio.apply()

        # Add an asyncio queue
        self.queue = asyncio.Queue()

    async def _run_stream_for_jupyter(self, api_request_json):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.hostname}{self.domain_path}", headers=self.headers, json=api_request_json) as resp:
                async for chunk in resp.content.iter_any():
                    await self.queue.put(chunk.decode('utf-8'))

    async def get_sequences(self):
        while True:
            sequence = await self.queue.get()

            # if sequence == '<<EOS>>':
            #     # End of stream
            #     break
            # Do something with the sequence
            # You can add a check here to break the loop when a certain condition is met
            print(sequence)
            # return sequence

    def run_stream_jupyter(self, api_request_json):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run_stream_for_jupyter(api_request_json))
        loop.run_until_complete(self.get_sequences())

    async def run_stream(self, api_request_json):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.hostname}{self.domain_path}", headers=self.headers, json=api_request_json) as resp:
                async for chunk in resp.content.iter_any():
                    yield chunk.decode('utf-8')

    def run_sync(self, api_request_json):
        response = requests.post(f"{self.hostname}{self.domain_path}", headers=self.headers, json=api_request_json)
        if response.status_code != 200:        
            raise Exception(f"POST {response.status_code} {response.json()['detail']}")
        return response  # assuming server responds with JSON
    

    def run_jupyter(self, api_request_json):
        if api_request_json.get('stream', False):
            return self.run_stream_jupyter(api_request_json)
        else:
            return self.run_sync(api_request_json)

    def run(self, api_request_json):
        if api_request_json.get('stream', False):
            return self.run_stream(api_request_json)
        else:
            return self.run_sync(api_request_json)
