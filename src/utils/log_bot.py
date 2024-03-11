import asyncio
import time
from typing import Iterable, Optional, Union

import httpx
from httpx import Response

from config import settings, VERSION

LOG_DELAY = settings.LOG_DELAY


class Bot:
    """Telegram Bot API interface to send messages to certain chats/users"""

    _API_HOST: str = "api.telegram.org"

    def __init__(self, bot_token: str, chat_id: str, timeout: int = 10, parse_mode: str = 'HTML'):
        self._token: str = bot_token
        self.chat_id: str = chat_id
        self.timeout: int = timeout
        self.parse_mode: str = parse_mode
        self.last_response_date = time.monotonic()


    async def send_message(self, message, chat_id: Optional[str] = None) -> Response:
        """Send message through Telegram bot."""
        if settings.SEND_LOGS:
            return await self._send_message(message, chat_id)

    async def send_error_report(self, message: Union[Exception, str], chat_id: Optional[str] = None) -> Response:
        """Send error message through Telegram bot."""
        if settings.SEND_ERRORS:
            return await self._send_message(f"[E] {message}", chat_id)

    async def send_document(
        self, files: Iterable, caption: str | None = None, chat_id: Optional[str] = None
    ) -> Response:
        """Send file through Telegram bot."""
        if settings.STAGE != "default":
            return await self._send_document(files, caption, chat_id)

    async def _send_message(self, message: str, chat_id: str = '') -> Response:
        """Send message through Telegram bot."""

        chat_id: str = chat_id if chat_id else self.chat_id
        if chat_id:
            headers: dict = {'Content-Type': 'application/json'}
            data: dict = {
                'chat_id': chat_id,
                'text': f'[{settings.PROJECT_NAME}] [{settings.STAGE}] [{VERSION}]: {message}',
                'parse_mode': self.parse_mode,
            }
            # logger.debug(f'Sending message via info bot... \nData: {data}')
            return await self._send_api_request('sendMessage', headers=headers, json=data)

    async def _send_document(self, files: Iterable, caption: str | None = None, chat_id: str = '') -> Response:
        """Send file as Telegram document."""

        chat_id: str = chat_id if chat_id else self.chat_id
        if chat_id:
            data: dict = {
                'chat_id': chat_id,
                'caption': caption if caption else '',
                'parse_mode': self.parse_mode,
            }
            # logger.debug(f'Sending document via info bot... \nData: {data}')

            return await self._send_api_request('sendDocument', headers={}, data=data, files=files)

    async def _send_api_request(self, api_method: str, headers: dict, *_, **kwargs) -> Response:
        if self._token:
            try:
                url: str = f'https://{self._API_HOST}/bot{self._token}/{api_method}'
                async with httpx.AsyncClient() as client:
                    last_response_date = time.monotonic()
                    if self.last_response_date + LOG_DELAY > last_response_date:
                        await asyncio.sleep(LOG_DELAY)
                    response = await client.post(url, headers=headers, timeout=self.timeout, **kwargs)
                    self.last_response_date = last_response_date
                    return response.json()

            except Exception as err:
                # logger.warning(f"SEND Bot error: {err}")
                print(f"SEND Bot error: {err}")


bot: Bot = Bot(bot_token=settings.TELEBOT_TOKEN, chat_id=settings.LOG_TG_CHANNEL)
