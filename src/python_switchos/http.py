from abc import ABC, abstractmethod

class HttpResponse(ABC):
    @property
    @abstractmethod
    def status(self) -> int:
        pass

    @abstractmethod
    def raise_for_status(self):
        pass

    @abstractmethod
    async def text(self) -> str:
        pass

class HttpClient(ABC):
    @abstractmethod
    async def get(self, url) -> HttpResponse:
        pass

try:
    import aiohttp

    class AioHttpResponse(HttpResponse):
        
        response: aiohttp.ClientResponse

        def __init__(self, response: aiohttp.ClientResponse):
            self.response = response

        async def __aenter__(self):
            return await self.response.__aenter__()

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            return await self.response.__aexit__(exc_type, exc_val, exc_tb)

        @property
        def status(self) -> int:
            return self.response.status

        def raise_for_status(self):
            return self.response.raise_for_status()

        async def text(self) -> str:
            return await self.response.text()

    class AioHttpClient(HttpClient):
        session: aiohttp.ClientSession

        def __init__(self, session: aiohttp.ClientSession):
            assert isinstance(session, aiohttp.ClientSession)
            self.session = session

        async def __aenter__(self):
            return await self.session.__aenter__()

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            return await self.session.__aexit__(exc_type, exc_val, exc_tb)
        
        async def get(self, url) -> HttpResponse:
            response = await self.session.get(url)
            return AioHttpResponse(response)

except ImportError:
    AioHttpClient = None

try:
    import httpx
    class HttpxResponse(HttpResponse):
        
        response: httpx.Response

        def __init__(self, response: httpx.Response):
            self.response = response

        async def __aenter__(self):
            return self.response

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

        @property
        def status(self) -> int:
            return self.response.status_code

        def raise_for_status(self):
            return self.response.raise_for_status()

        async def text(self) -> str:
            return self.response.text

    class HttpxClient(HttpClient):
        client: httpx.AsyncClient

        def __init__(self, client: httpx.AsyncClient, auth: httpx.DigestAuth | httpx.UseClientDefault):
            assert isinstance(client, httpx.AsyncClient)
            self.client = client
            self.auth = auth

        async def __aenter__(self):
            return await self.client.__aenter__()

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            return await self.client.__aexit__(exc_type, exc_val, exc_tb)
        
        async def get(self, url) -> HttpResponse:
            response = await self.client.get(url, auth=self.auth)
            return HttpxResponse(response)
            
except ImportError:
    HttpxClient = None

def create_aiohttp_client(client) -> HttpClient:
    assert AioHttpClient is not None and isinstance(client, aiohttp.ClientSession)
    return AioHttpClient(client)

def create_httpx_client(client, auth=None) -> HttpClient:
    assert HttpxClient is not None and isinstance(client, httpx.AsyncClient)
    if auth is None:
        auth = httpx.USE_CLIENT_DEFAULT
    return HttpxClient(client, auth)