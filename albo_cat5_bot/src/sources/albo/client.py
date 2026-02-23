from __future__ import annotations

import time
from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config import settings


class AlboClient:
    """Client with conservative throttling and explicit user-agent."""

    def __init__(self, base_url: str = "https://www.albonazionalegestoriambientali.it") -> None:
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            headers={"User-Agent": settings.user_agent},
            timeout=settings.timeout_seconds,
            follow_redirects=True,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def get(self, path: str, params: dict[str, Any] | None = None) -> httpx.Response:
        time.sleep(settings.request_delay_seconds)
        return self._client.get(f"{self.base_url}/{path.lstrip('/')}", params=params)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def post(self, path: str, data: dict[str, Any]) -> httpx.Response:
        time.sleep(settings.request_delay_seconds)
        return self._client.post(f"{self.base_url}/{path.lstrip('/')}", data=data)

    def close(self) -> None:
        self._client.close()
