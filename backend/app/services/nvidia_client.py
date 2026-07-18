"""NVIDIA AI API client for MindMirror AI."""

import httpx
import logging
from typing import Optional

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class NVIDIAAIClient:
    """Client for NVIDIA AI API."""

    def __init__(self):
        settings = get_settings()

        self.api_key = settings.nvidia_api_key

        self.base_url = "https://integrate.api.nvidia.com/v1"

        self.timeout = httpx.Timeout(
            connect=10.0,
            read=60.0,
            write=10.0,
            pool=10.0
        )

        self.client = httpx.AsyncClient(
            timeout=self.timeout
        )

        if not self.api_key:
            logger.warning(
                "NVIDIA API key is missing. AI responses will fallback."
            )


    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str = "meta/llama-3.1-70b-instruct",
        temperature: float = 0.6,
        max_tokens: int = 2048,
    ) -> Optional[str]:

        if not self.api_key:
            logger.error("NVIDIA API key not configured")
            return None


        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }


        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }


        try:

            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )


            if response.status_code != 200:
                logger.error(
                    f"NVIDIA API failed: "
                    f"{response.status_code} "
                    f"{response.text}"
                )
                return None


            data = response.json()


            if (
                "choices" not in data
                or len(data["choices"]) == 0
            ):
                logger.error(
                    "Invalid NVIDIA response format"
                )
                return None


            return (
                data["choices"][0]
                ["message"]
                ["content"]
            )


        except httpx.TimeoutException:

            logger.error(
                "NVIDIA API timeout"
            )
            return None


        except httpx.RequestError as e:

            logger.error(
                f"NVIDIA request error: {e}"
            )
            return None


        except Exception as e:

            logger.exception(
                f"Unexpected NVIDIA error: {e}"
            )
            return None



    async def close(self):

        await self.client.aclose()



# Singleton

_nvidia_client: Optional[NVIDIAAIClient] = None



def get_nvidia_client() -> NVIDIAAIClient:

    global _nvidia_client


    if _nvidia_client is None:

        _nvidia_client = NVIDIAAIClient()


    return _nvidia_client