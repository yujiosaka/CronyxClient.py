from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest

from cronyx_client.error import CronyxClientError
from cronyx_client.job_client import JobClient
from cronyx_client.job_runner import JobRunner
from cronyx_client.schema import PostResponse


class TestJobRunner:
    @pytest.fixture
    def job_id(self):
        return "6541d97684f72238cf3dc0ab"

    @pytest.fixture
    def job_name(self):
        return "jobName"

    @pytest.fixture
    def job_interval(self):
        return 1000 * 60 * 60 * 24  # 1 day

    @pytest.fixture
    def job_response(self, job_id, job_name, job_interval):
        requested_at = datetime.fromisoformat("2023-02-03T15:00:00.000")
        job_interval_started_at = requested_at - timedelta(days=1)
        job_interval_ended_at = requested_at
        return PostResponse.model_validate(
            {
                "id": job_id,
                "name": job_name,
                "interval": job_interval,
                "intervalStartedAt": job_interval_started_at.isoformat(),
                "intervalEndedAt": job_interval_ended_at.isoformat(),
                "isActive": True,
                "createdAt": requested_at.isoformat(),
                "updatedAt": requested_at.isoformat(),
            }
        )

    @pytest.fixture
    def job_client(self):
        return MagicMock(spec=JobClient)

    @pytest.fixture
    def job_runner(self, job_client, job_name, job_interval):
        return JobRunner(job_client, job_name, job_interval)

    class TestRequestJobStart:
        @pytest.mark.asyncio
        async def test_does_not_start_job(self, job_client, job_runner):
            job_client.post.return_value = None

            job = await job_runner.request_job_start()

            assert job is None

        @pytest.mark.asyncio
        async def test_fails_to_start_job(self, job_client, job_runner):
            job_client.post.side_effect = Exception("Failed to post")

            with pytest.raises(CronyxClientError, match="Cannot activate job lock for jobName"):
                await job_runner.request_job_start()

        @pytest.mark.asyncio
        async def test_starts_job(self, job_client, job_runner, job_response):
            job_client.post.return_value = job_response

            job = await job_runner.request_job_start()

            assert job.id == job_response.id
            assert job.name == job_response.name
            assert job.interval == job_response.interval
            assert job.interval_started_at == job_response.interval_started_at
            assert job.interval_ended_at == job_response.interval_ended_at
            assert job.is_active == job_response.is_active
            assert job.created_at == job_response.created_at
            assert job.updated_at == job_response.updated_at

    class TestRequestJobExec:
        @pytest.mark.asyncio
        async def test_does_not_execute_job(self, job_client, job_runner):
            job_client.post.return_value = None
            job_task = AsyncMock()

            await job_runner.request_job_exec(job_task)

            assert job_client.post.call_count == 1
            assert job_client.put.call_count == 0
            assert job_task.call_count == 0

        @pytest.mark.asyncio
        async def test_fails_to_start_job(self, job_client, job_runner):
            job_client.post.side_effect = Exception("Failed to post")
            job_task = AsyncMock()

            with pytest.raises(CronyxClientError, match="Cannot activate job lock for jobName"):
                await job_runner.request_job_exec(job_task)

            assert job_client.post.call_count == 1
            assert job_client.put.call_count == 0
            assert job_task.call_count == 0

        @pytest.mark.asyncio
        async def test_executes_job(self, job_client, job_runner, job_response):
            job_client.post.return_value = job_response
            job_task = AsyncMock()

            await job_runner.request_job_exec(job_task)

            assert job_client.post.call_count == 1
            assert job_client.put.call_count == 1
            assert job_task.call_count == 1

        @pytest.mark.asyncio
        async def test_fails_to_finish_job(self, job_client, job_runner, job_response):
            job_client.post.return_value = job_response
            job_client.put.side_effect = Exception("Failed to put")
            job_task = AsyncMock()

            with pytest.raises(CronyxClientError, match="Cannot finish job for jobName"):
                await job_runner.request_job_exec(job_task)

            assert job_client.post.call_count == 1
            assert job_client.put.call_count == 1
            assert job_task.call_count == 1

        @pytest.mark.asyncio
        async def test_interrupts_job(self, job_client, job_runner, job_response):
            job_client.post.return_value = job_response
            job_task = AsyncMock(side_effect=Exception("Something went wrong"))

            with pytest.raises(Exception, match="Something went wrong"):
                await job_runner.request_job_exec(job_task)

            assert job_client.post.call_count == 1
            assert job_client.put.call_count == 1
            assert job_task.call_count == 1

        @pytest.mark.asyncio
        async def test_fails_to_interrupt_job(self, job_client, job_runner, job_response):
            job_client.post.return_value = job_response
            job_client.put.side_effect = Exception("Failed to put")
            job_task = AsyncMock(side_effect=Exception("Something went wrong"))

            with pytest.raises(Exception, match="Cannot interrupt job for jobName"):
                await job_runner.request_job_exec(job_task)

            assert job_client.post.call_count == 1
            assert job_client.put.call_count == 1
            assert job_task.call_count == 1
