import asyncio
from getpass import getpass
from httpx import AsyncClient, DigestAuth
from python_switchos.client import Client
from python_switchos.endpoints.link import LinkEndpoint
from python_switchos.endpoints.sys import SystemEndpoint
from python_switchos.endpoints.poe import PoEEndpoint
from python_switchos.http import create_httpx_client

async def fetchAndPrint(client: Client, cls):
    response = await client.fetch(cls)
    print(response)

async def main(host, user, password):
    auth = DigestAuth(user, password)
    async with AsyncClient(auth=auth) as session:
        client = Client(create_httpx_client(session), host)
        await fetchAndPrint(client, SystemEndpoint)
        await fetchAndPrint(client, LinkEndpoint)
        await fetchAndPrint(client, PoEEndpoint)

if __name__ == "__main__":
    asyncio.run(main(input("Host: "), input("User: "), getpass("Password: ")))