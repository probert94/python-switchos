from typing import Type, TypeVar
from urllib.parse import urljoin

from python_switchos.endpoint import SwitchOSEndpoint, readDataclass
from python_switchos.http import HttpClient

T = TypeVar("T", bound=SwitchOSEndpoint)

class Client:
    """Client to connect to the available endpoints"""
    host: str
    httpClient: HttpClient

    def __init__(self, httpClient: HttpClient, host: str):
        self.httpClient = httpClient
        self.host = host.rstrip("/") + "/"  # Make sure host ends with a single "/"

    async def fetch(self, cls: Type[T]) -> T:
        response = await self.httpClient.get(urljoin(self.host, cls.endpoint_path))
        async with response:
            response.raise_for_status()
            text = await response.text()
            return readDataclass(cls, text)
