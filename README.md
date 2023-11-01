# CronyxClient.py [![PyPI version](https://badge.fury.io/py/cronyx-client.svg)](https://badge.fury.io/py/cronyx-client) [![CI/CD](https://github.com/yujiosaka/CronyxClient.py/actions/workflows/ci_cd.yml/badge.svg)](https://github.com/yujiosaka/CronyxClient.py/actions/workflows/ci_cd.yml)

###### [API](https://github.com/yujiosaka/CronyxClient.py/blob/main/docs/API.md) | [Code of Conduct](https://github.com/yujiosaka/CronyxClient.py/blob/main/docs/CODE_OF_CONDUCT.md) | [Contributing](https://github.com/yujiosaka/CronyxClient.py/blob/main/docs/CONTRIBUTING.md) | [Changelog](https://github.com/yujiosaka/CronyxClient.py/blob/main/docs/CHANGELOG.md)

A Python HTTP client wrapper for [CronyxServer](https://github.com/yujiosaka/CronyxServer), seamlessly integrating the power of [Cronyx](https://github.com/yujiosaka/Cronyx) across platforms using a familiar API interface.

## 🌟 Features

<img src="https://github.com/yujiosaka/CronyxClient.py/assets/2261067/08e074cf-9256-4b15-ae14-f3e607165f54" alt="icon" width="300" align="right">

CronyxClient.py bridges the capabilities of Cronyx and CronyxServer, offering a way to schedule and manage tasks without losing the feel of the original [Cronyx API](https://github.com/yujiosaka/Cronyx/blob/main/docs/API.md).

### Why CronyxClient.py?

🌐 **Unified Experience**: Retain the simplicity and power of the Cronyx API while benefiting from the language-agnostic capabilities of CronyxServer.

🔌 **Plug & Play**: With just a URL configuration, connect to any running instance of CronyxServer and harness its capabilities without changing your existing Cronyx codebase.

🚀 **Familiar API with Async/Await**: Use the same API calls you're familiar with from Cronyx, with the added advantage of Python's `async` and `await` syntax for handling asynchronous operations.

## 🚀 Getting Started

### Installation

Install the CronyxClient.py package using pip:

```sh
$ pip install cronyx-client
# or
# $ poetry add cronyx-client
```

### Basic Usage

#### 1. Manually Handling Job Execution:

CronyxClient.py mirrors the usage of Cronyx, with the additional specification of the CronyxServer URL:

```py
from cronyx_client import CronyxClient

cronyx = CronyxClient(url="http://localhost:3000/")
job = await cronyx.request_job_start(
  job_name="hourly-job",
  job_interval="0 * * * *",
)

# Check if the job is due to run
if job:
  try:
    print(job.interval_started_at)
    print(job.interval_ended_at)
    await job.finish()
  except Exception as e:
    await job.interrupt()
```

#### 2. Using the Shorthand Callback:

```py
from cronyx_client import CronyxClient

async def task(job):
    print(job.interval_started_at)
    print(job.interval_ended_at)

cronyx = CronyxClient(url="http://localhost:3000/")
await cronyx.request_job_exec(
  job_name="hourly-job",
  job_interval="0 * * * *",
  task=task
)
```

### Integrations and Compatibilities

CronyxClient.py is built on top of the Cronyx foundation, ensuring compatibility and integration with:

- **Cronyx**: Maintain the same API functions and structures, ensuring a seamless transition to CronyxClient.py.
- **CronyxServer**: Directly communicates with the server using its RESTful endpoints, translating your Cronyx API calls to HTTP requests.

## 💻 Development

Using Visual Studio Code and the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension, you can simplify the development environment setup process. The extension allows you to develop inside a Docker container and automatically sets up the development environment for you.

1. Install the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension in Visual Studio Code.

2. Clone the repository:

```sh
git clone https://github.com/yujiosaka/CronyxClient.py.git
```

3. Open the cloned repository in Visual Studio Code.

4. When prompted by Visual Studio Code, click "Reopen in Container" to open the project inside the Docker container.

5. The extension will build the Docker container and set up the development environment for you. This may take a few minutes.

6. Build and run the Docker container with Docker Compose:

```sh
$ docker-compose up --build
```

This will start testing in watch mode.

## 🧑‍💻️ API reference

See [here](https://github.com/yujiosaka/CronyxClient.py/blob/main/docs/API.md) for the API reference.

## 🐞 Debugging tips

### Enable debug logging

Configure the log level using the `LOG_LEVEL` environment variable.

```sh
env LOG_LEVEL="DEBUG" python script.py
```

CronyxClient.py utilizes Python's `logging` module for logging debug messages. Ensure that you have the logger configured in your application to capture these logs.

## 💳 License

This project is licensed under the MIT License. See [LICENSE](https://github.com/yujiosaka/Cronyx/blob/main/LICENSE) for details.
