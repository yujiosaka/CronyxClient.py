from datetime import datetime
from typing import Awaitable, Callable, List, Optional, Union

from .job import Job
from .job_client import JobClient
from .job_runner import JobRunner
from .options import Credentials, Duration


class CronyxClient:
    def __init__(self, url: str, credentials: Optional[Credentials] = None) -> None:
        self._job_client = JobClient(url, credentials)

    async def request_job_exec(
        self,
        job_name: str,
        task: Callable[[Job], Awaitable[None]],
        job_interval: Union[Duration, str, int],
        start_buffer: Optional[Union[Duration, int]] = None,
        retry_interval: Optional[Union[Duration, int]] = None,
        required_job_names: Optional[List[str]] = None,
        timezone: Optional[str] = None,
        no_lock: Optional[bool] = None,
        job_interval_started_at: Optional[datetime] = None,
    ) -> None:
        job_runner = JobRunner(
            self._job_client,
            job_name,
            job_interval,
            timezone=timezone,
            required_job_names=required_job_names,
            start_buffer=start_buffer,
            retry_interval=retry_interval,
            no_lock=no_lock,
            job_interval_started_at=job_interval_started_at,
        )
        return await job_runner.request_job_exec(task)

    async def request_job_start(
        self,
        job_name: str,
        job_interval: Union[Duration, str, int],
        start_buffer: Optional[Union[Duration, int]] = None,
        retry_interval: Optional[Union[Duration, int]] = None,
        required_job_names: Optional[List[str]] = None,
        timezone: Optional[str] = None,
        no_lock: Optional[bool] = None,
        job_interval_started_at: Optional[datetime] = None,
    ) -> Optional[Job]:
        job_runner = JobRunner(
            self._job_client,
            job_name,
            job_interval,
            timezone=timezone,
            required_job_names=required_job_names,
            start_buffer=start_buffer,
            retry_interval=retry_interval,
            no_lock=no_lock,
            job_interval_started_at=job_interval_started_at,
        )
        return await job_runner.request_job_start()
