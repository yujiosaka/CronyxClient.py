from datetime import datetime, timedelta
from typing import Awaitable, Callable, List, Optional, Union
from urllib import parse

from .error import CronyxClientError
from .job import Job
from .job_client import JobClient
from .options import Credentials, Duration
from .schema import PostBody


class JobRunner:
    def __init__(
        self,
        job_client: JobClient,
        job_name: str,
        job_interval: Union[timedelta, str, int],
        timezone: Optional[str] = None,
        required_job_names: Optional[List[str]] = None,
        start_buffer: Optional[Union[Duration, int]] = None,
        retry_interval: Optional[Union[Duration, int]] = None,
        no_lock: Optional[bool] = None,
        job_interval_started_at: Optional[datetime] = None,
        credentials: Optional[Credentials] = None,
    ):
        self._job_client = job_client
        self._job_name = job_name
        self._job_interval = job_interval
        self._timezone = timezone
        self._required_job_names = required_job_names
        self._start_buffer = start_buffer
        self._retry_interval = retry_interval
        self._no_lock = no_lock
        self._job_interval_started_at = job_interval_started_at

    async def request_job_exec(self, task: Callable[[Job], Awaitable[None]]) -> None:
        job = await self.request_job_start()
        if not job:
            return

        try:
            await task(job)
        except Exception as error:
            await job.interrupt()
            raise error

        await job.finish()

    async def request_job_start(self) -> Optional[Job]:
        try:
            job_name = parse.quote(self._job_name)
            job_lock = await self._job_client.post(
                f"/{job_name}",
                PostBody(
                    job_interval=self._job_interval,
                    timezone=self._timezone,
                    required_job_names=self._required_job_names,
                    start_buffer=self._start_buffer,
                    retry_interval=self._retry_interval,
                    no_lock=self._no_lock,
                    job_interval_started_at=self._job_interval_started_at,
                ),
            )
            if not job_lock:
                return None

            return Job(self._job_client, job_lock)
        except Exception as error:
            raise CronyxClientError(f"Cannot activate job lock for {self._job_name}", error)
