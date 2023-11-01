import asyncio
from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from cronyx_client.error import CronyxClientError
from cronyx_client.job import Job
from cronyx_client.job_client import JobClient
from cronyx_client.schema import PostResponse


class TestJob:
    @pytest.fixture
    def job_id(self, request):
        if request.param:
            return None
        else:
            return "6541d97684f72238cf3dc0ab"

    @pytest.fixture
    def job_name(self):
        return "jobName"

    @pytest.fixture
    def job_interval(self):
        return 1000 * 60 * 60  # 1 hour

    @pytest.fixture
    def job_lock(self, job_id, job_name, job_interval):
        now = datetime.now()
        job_interval_started_at = now - timedelta(hours=1)
        job_interval_ended_at = now

        return PostResponse.model_validate(
            {
                "id": job_id,
                "name": job_name,
                "interval": job_interval,
                "intervalStartedAt": job_interval_started_at.isoformat(),
                "intervalEndedAt": job_interval_ended_at.isoformat(),
                "isActive": True,
                "createdAt": now.isoformat(),
                "updatedAt": now.isoformat(),
            }
        )

    @pytest.fixture
    def job_client(self):
        return MagicMock(spec=JobClient)

    @pytest.fixture
    def job(self, job_client, job_lock):
        return Job(job_client, job_lock)

    @pytest.mark.parametrize("job_id", [False, True], indirect=True)
    def test_id(self, job, job_lock):
        assert job.id == job_lock.id

    @pytest.mark.parametrize("job_id", [False, True], indirect=True)
    def test_name(self, job, job_lock):
        assert job.name == job_lock.name

    @pytest.mark.parametrize("job_id", [False, True], indirect=True)
    def test_interval(self, job, job_lock):
        assert job.interval == job_lock.interval

    @pytest.mark.parametrize("job_id", [False, True], indirect=True)
    def test_interval_started_at(self, job, job_lock):
        assert job.interval_started_at == job_lock.interval_started_at

    @pytest.mark.parametrize("job_id", [False, True], indirect=True)
    def test_interval_ended_at(self, job, job_lock):
        assert job.interval_ended_at == job_lock.interval_ended_at

    @pytest.mark.parametrize("job_id", [False, True], indirect=True)
    def test_is_active(self, job, job_lock):
        assert job.is_active == job_lock.is_active

    @pytest.mark.parametrize("job_id", [False, True], indirect=True)
    def test_created_at(self, job, job_lock):
        assert job.created_at == job_lock.created_at

    @pytest.mark.parametrize("job_id", [False, True], indirect=True)
    def test_updated_at(self, job, job_lock):
        assert job.updated_at == job_lock.updated_at

    @pytest.mark.asyncio
    @pytest.mark.parametrize("job_id", [False, True], indirect=True)
    async def test_finish_job(self, job, job_client, job_id):
        await job.finish()

        if job_id:
            assert job_client.put.call_count == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize("job_id", [False, True], indirect=True)
    async def test_interrupt_job(self, job, job_client, job_id):
        await job.interrupt()

        if job_id:
            assert job_client.put.call_count == 1

    class TestAfterFinishingJob:
        @pytest.fixture
        def setup(self, job):
            asyncio.run(job.finish())

        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        def test_fails_to_get_id(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                job.id

        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        def test_fails_to_get_name(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                job.name

        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        def test_fails_to_get_interval(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                job.interval

        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        def test_fails_to_get_interval_started_at(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                job.interval_started_at

        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        def test_fails_to_get_interval_ended_at(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                job.interval_ended_at

        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        def test_fails_to_get_is_active(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                job.is_active

        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        def test_fails_to_get_created_at(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                job.created_at

        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        def test_fails_to_get_updated_at(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                job.updated_at

        @pytest.mark.asyncio
        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        async def test_fails_to_finish_job(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                await job.finish()

        @pytest.mark.asyncio
        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        async def test_fails_to_interrupt_job(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                await job.interrupt()

    class TestAfterInterruptingJob:
        @pytest.fixture
        def setup(self, job):
            asyncio.run(job.interrupt())

        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        def test_fails_to_get_id(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                job.id

        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        def test_fails_to_get_name(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                job.name

        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        def test_fails_to_get_interval(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                job.interval

        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        def test_fails_to_get_interval_started_at(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                job.interval_started_at

        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        def test_fails_to_get_interval_ended_at(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                job.interval_ended_at

        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        def test_fails_to_get_is_active(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                job.is_active

        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        def test_fails_to_get_created_at(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                job.created_at

        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        def test_fails_to_get_updated_at(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                job.updated_at

        @pytest.mark.asyncio
        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        async def test_fails_to_finish_job(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                await job.finish()

        @pytest.mark.asyncio
        @pytest.mark.parametrize("job_id", [False, True], indirect=True)
        async def test_fails_to_interrupt_job(self, setup, job):
            with pytest.raises(CronyxClientError, match="Job is not active for jobName"):
                await job.interrupt()

    class TestWhenDeactivatingJobLockFails:
        @pytest.fixture
        def setup(self, job_client):
            job_client.put.side_effect = Exception("Request failed")

        @pytest.mark.asyncio
        @pytest.mark.parametrize("job_id", [False], indirect=True)
        async def test_fails_to_finish_job(self, setup, job):
            with pytest.raises(CronyxClientError, match="Cannot finish job for jobName"):
                await job.finish()

    class TestWhenInterruptingJobLockFails:
        @pytest.fixture
        def setup(self, job_client):
            job_client.put.side_effect = Exception("Request failed")

        @pytest.mark.asyncio
        @pytest.mark.parametrize("job_id", [False], indirect=True)
        async def test_fails_to_interrupt_job(self, setup, job):
            with pytest.raises(CronyxClientError, match="Cannot interrupt job for jobName"):
                await job.interrupt()
