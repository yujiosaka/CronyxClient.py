from typing import Optional, TypedDict, Union
from urllib import parse

import httpx

from .options import Credentials, Duration
from .schema import PostBody, PostResponse


class PostBodyRequired(TypedDict):
    job_interval: Union[str, int, Duration]


class JobClient:
    def __init__(self, url: str, credentials: Optional[Credentials] = None) -> None:
        self._url = url
        self._headers = {"Content-Type": "application/json"}
        self._auth = None
        if credentials:
            self.auth = (credentials["username"], credentials["password"])

    async def post(self, path: str, body: PostBody) -> Optional[PostResponse]:
        url = parse.urljoin(self._url, path)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, json=body.model_dump(exclude_none=True), headers=self._headers, auth=self._auth
            )
            response.raise_for_status()

            if not response:
                return None

            return PostResponse.model_validate(response.json())

    async def put(self, path: str) -> None:
        url = parse.urljoin(self._url, path)
        async with httpx.AsyncClient() as client:
            response = await client.put(url, headers=self._headers, auth=self._auth)
            response.raise_for_status()
