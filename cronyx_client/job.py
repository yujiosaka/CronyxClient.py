import asyncio
from datetime import datetime
from typing import Awaitable, Optional
from urllib import parse

from .error import CronyxClientError
from .job_client import JobClient
from .schema import PostResponse
from .util import log


class Job:
    def __init__(self, job_client: JobClient, job_lock: PostResponse):
        self._job_name = job_lock.name
        self._job_client = job_client
        self._job_lock = job_lock
        self._pending_promise: Optional[Awaitable[None]] = None

    @property
    def id(self) -> Optional[str]:
        self._check_active()

        return self._job_lock.id

    @property
    def name(self) -> str:
        self._check_active()

        return self._job_lock.name

    @property
    def interval(self) -> int:
        self._check_active()

        return self._job_lock.interval

    @property
    def interval_started_at(self) -> datetime:
        self._check_active()

        return self._job_lock.interval_started_at

    @property
    def interval_ended_at(self) -> datetime:
        self._check_active()

        return self._job_lock.interval_ended_at

    @property
    def is_active(self) -> bool:
        self._check_active()

        return self._job_lock.is_active

    @property
    def created_at(self) -> datetime:
        self._check_active()

        return self._job_lock.created_at

    @property
    def updated_at(self) -> datetime:
        self._check_active()

        return self._job_lock.updated_at

    async def finish(self) -> None:
        self._check_active()
        self._check_pending()

        job_id = self._job_lock.id
        if job_id is None:
            self._job_lock = self._job_lock.model_copy(update={"is_active": False})
            return

        job_name = parse.quote(self._job_name)
        job_id = parse.quote(job_id)

        async def finish_task():
            nonlocal self
            try:
                await self._job_client.put(f"/{job_name}/{job_id}/finish")
                log(f"Job is finished for {self._job_name}")
                self._job_lock = None
            except Exception as error:
                raise CronyxClientError(f"Cannot finish job for {self._job_name}", error)
            finally:
                self._pending_promise = None

        self._pending_promise = asyncio.ensure_future(finish_task())
        await self._pending_promise

    async def interrupt(self) -> None:
        self._check_active()
        self._check_pending()

        job_id = self._job_lock.id
        if job_id is None:
            self._job_lock = None
            return

        job_name = parse.quote(self._job_name)
        job_id = parse.quote(job_id)

        async def interrupt_task():
            nonlocal self
            try:
                await self._job_client.put(f"/{job_name}/{job_id}/interrupt")
                log(f"Job is interrupted for {self._job_name}")
                self._job_lock = None
            except Exception as error:
                raise CronyxClientError(f"Cannot interrupt job for {self._job_name}", error)
            finally:
                self._pending_promise = None

        self._pending_promise = asyncio.ensure_future(interrupt_task())
        await self._pending_promise

    def _check_active(self):
        if not self._job_lock or not self._job_lock.is_active:
            raise CronyxClientError(f"Job is not active for {self._job_name}")

    def _check_pending(self):
        if self._pending_promise:
            raise CronyxClientError(f"Job is pending for {self._job_name}")
