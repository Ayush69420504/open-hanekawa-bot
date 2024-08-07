import aiohttp,asyncio,time
import requests

async def upload(fp, expires):
    file = open(fp, "rb")
    data = aiohttp.FormData()
    data.add_field('file', file)
    data.add_field('expires', str(int(time.time()+expires)))
    session = aiohttp.ClientSession()
    response = await session.post(url='https://0x0.st', data=data)
    data = await response.content.read()
    url = data.decode("UTF-8").strip()
    await session.close()
    return url
