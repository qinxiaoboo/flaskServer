from typing import Dict
from web3.providers.async_rpc import AsyncHTTPProvider


class AsyncHTTPProviderWithUA(AsyncHTTPProvider):

    def __init__(
        self,
        useragent,
        endpoint_uri: str = None,
        request_kwargs=None,
    ) -> None:
        super().__init__(endpoint_uri, request_kwargs)
        self.useragent = useragent

    def get_request_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "User-Agent": self.useragent,
        }
