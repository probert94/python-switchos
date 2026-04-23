# python-switchos
Python library to interact with MikroTik SwitchOS and SwitchOS Lite

## Features

- Get identity, model, serial number, OS version, MAC and IP address

- Read cpu temperature, current, voltage, and power consumption of the switch

- List ports with name, status, speed, duplex mode etc.

- Check PoE status, power usage, voltage, and current per port

## Installation

Install via pip:

```bash
pip install python-switchos
```

> Requires Python 3.10 or higher

## Dependencies

- demjson3 3.0.6 or higher - for tolerant JSON parsing

## Usage Example


Example with httpx

```python
async def main(host, user, password):
    auth = DigestAuth(user, password)
    async with AsyncClient(auth=auth) as session:
        client = Client(create_httpx_client(session), host)
        print(await client.fetch(SystemEndpoint))
```

Example with aiohttp

```python
async def main(host, user, password):
    digest_auth = DigestAuthMiddleware(login=user, password=password)
    async with ClientSession(middlewares=(digest_auth, )) as session:
        client = Client(create_aiohttp_client(session), host)
        return await client.fetch(SystemEndpoint)
```

## Supported Devices

This library targets MikroTik switches running **SwitchOS** or **SwitchOS Lite** and has been tested with:
- Mikrotik CRS326-24G-2S+ running Switch OS 2.18
- MikroTik CSS610-8P-2S+ running Switch OS Lite 2.20 and 2.21

Other models with SwitchOS or SwitchOS Lite may also work.

## License

MIT License

## Contributing

Contributions are welcome!\
Feel free to open issues, submit pull requests, or suggest features.

