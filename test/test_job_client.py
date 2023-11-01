from datetime import datetime, timedelta

import httpx
import pytest

from cronyx_client.job_client import JobClient
from cronyx_client.schema import PostBody, PostResponse


class TestJobClient:
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
    def post_body(self):
        return PostBody(job_interval="0 0 0 * *")  # daily

    @pytest.fixture
    def post_response(self, job_id, job_name, job_interval):
        requested_at = datetime.fromisoformat("2023-02-03T15:00:00.000Z")
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
    def url(self):
        return "http://localhost:3000"

    @pytest.fixture
    def credentials(self):
        return {"username": "user", "password": "pass"}

    @pytest.fixture
    def post_path(self, job_name):
        return f"{job_name}"

    @pytest.fixture
    def put_path(self, job_id, job_name):
        return f"/{job_name}/{job_id}/finish"

    @pytest.fixture
    def job_client(self, url, credentials):
        return JobClient(url, credentials=credentials)

    class TestPost:
        @pytest.mark.asyncio
        async def test_activates_job(self, mocker, job_client, post_path, post_body, post_response):
            post = mocker.patch("httpx.AsyncClient.post", return_value=MockResponse(status_code=200, json=post_response))

            response = await job_client.post(post_path, post_body)

            assert post.call_count == 1
            assert response.id == post_response.id
            assert response.name == post_response.name
            assert response.interval == post_response.interval
            assert response.interval_started_at == post_response.interval_started_at
            assert response.interval_ended_at == post_response.interval_ended_at
            assert response.is_active == post_response.is_active
            assert response.created_at == post_response.created_at
            assert response.updated_at == post_response.updated_at

        @pytest.mark.asyncio
        async def test_fails_to_activate_job(self, mocker, job_client, post_path, post_body):
            mocker.patch("httpx.AsyncClient.post", return_value=MockResponse(status_code=500))

            with pytest.raises(httpx.HTTPStatusError) as e:
                await job_client.post(post_path, post_body)

            assert str(e.value) == "Request failed"

    class TestPut:
        @pytest.mark.asyncio
        async def test_finishes_job(self, mocker, job_client, put_path):
            put = mocker.patch("httpx.AsyncClient.put", return_value=MockResponse(status_code=200))

            await job_client.put(put_path)

            assert put.call_count == 1

        @pytest.mark.asyncio
        async def test_fails_to_finish_job(self, mocker, job_client, put_path):
            mocker.patch("httpx.AsyncClient.put", return_value=MockResponse(status_code=500))

            with pytest.raises(httpx.HTTPStatusError) as e:
                await job_client.put(put_path)

            assert str(e.value) == "Request failed"


class MockResponse(httpx.Response):
    def __init__(self, status_code: int, json: dict = None):
        super().__init__(status_code=status_code, content=None)
        self._json = json

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code < 200 or self.status_code >= 300:
            raise httpx.HTTPStatusError("Request failed", request=None, response=self)
