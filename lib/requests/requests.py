import httpx
import json

class Response:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def json(self):
        return json.loads(self.text)

async def get(url, headers=None, params=None) -> Response:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        return Response(response.status_code, response.text)

async def post(url, headers=None, data=None, json=None) -> Response:
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=json, data=data)
        return Response(response.status_code, response.text)
