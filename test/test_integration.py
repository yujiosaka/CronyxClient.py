import os
from datetime import datetime

import pytest
from pymongo import MongoClient

from cronyx_client.cronyx_client import CronyxClient


class TestIntegration:
    @pytest.fixture
    def job_name(self):
        return "jobName"

    @pytest.fixture
    def job_interval(self):
        return 1000 * 60 * 60 * 24  # 1 day

    @pytest.fixture(scope="module")
    def mongo_client(self):
        client = MongoClient(os.environ["MONGO_URI"])
        yield client
        client.close()

    @pytest.fixture
    def delete_collection(self, mongo_client):
        mongo_client.test.joblocks.delete_many({})
        yield
        mongo_client.test.joblocks.delete_many({})

    @pytest.fixture
    def cronyx_client(self):
        return CronyxClient(os.environ["SERVER_URL"])

    @pytest.mark.asyncio
    async def test_runs_job(self, cronyx_client, job_name, job_interval, delete_collection):
        job = await cronyx_client.request_job_start(job_name=job_name, job_interval=job_interval)
        assert job.id is not None
        assert job.name == job_name
        assert job.interval <= job_interval
        assert type(job.interval_started_at) is datetime
        assert type(job.interval_ended_at) is datetime
        assert job.is_active is True
        assert type(job.created_at) is datetime
        assert type(job.updated_at) is datetime
        await job.finish()

    @pytest.mark.asyncio
    async def test_executes_job(self, cronyx_client, job_name, job_interval, mocker, delete_collection):
        job_task = mocker.AsyncMock()

        await cronyx_client.request_job_exec(job_name=job_name, job_interval=job_interval, task=job_task)

        assert job_task.call_count == 1
