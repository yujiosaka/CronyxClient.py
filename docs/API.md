# API Reference

## Table of Contents

- [CronyxClient Class](#cronyxclient-class)
  - [Constructor](#constructor)
  - [Methods](#methods)
- [Job Class](#job-class)
  - [Properties](#properties)
  - [Methods](#methods-1)

## CronyxClient Class

The `CronyxClient` class is responsible for managing the lifecycle of jobs, initiating, and executing tasks based on given criteria.

### Constructor

```python
def __init__(self, url: str, credentials: Optional[Credentials] = None) -> None:
```

**Parameters**:

- `url`: [str] - CronyxServer's location (e.g. `"http://localhost:3000/"`).
- `credentials` (**optional**):
  - `username`: [str] - CronyxServer's basic authentication user name
  - `password`: [str] - CronyxServer's basic authentication password

### Methods

#### `request_job_start`

Initiate the job based on the specified criteria.

```python
async def request_job_start(
    self,
    job_name: str,
    job_interval: Union[Duration, str, int],
    start_buffer: Optional[Union[Duration, int]] = None,
    retry_interval: Optional[Union[Duration, int]] = None,
    required_job_names: Optional[List[str]] = None,
    timezone: Optional[str] = None,
    no_lock: Optional[bool] = None,
    job_interval_started_at: Optional[datetime] = None
) -> Optional[Job]:
```

**Parameters**:

- `job_name`: [str] - A unique identifier for the series of jobs.
- `job_interval`: [Union]\[[Duration], [str], [int]\] - Specifies how frequently the job runs.
- `start_buffer` (**optional**): [Union]\[[Duration], [int]\] - Adds a delay before the job starts.
- `retry_interval` (**optional**): [Union]\[[Duration], [int]\] - Allows bypassing of an active job lock after a specified period.
- `required_job_names` (**optional**): [List]\[[str]\] - Specifies dependencies using their job names.
- `timezone` (**optional**): [str] - Overrides `timezone` of the constructor argument.
- `no_lock` (**optional**): [bool] - Bypasses job locks, letting other processes run the job.
- `job_interval_started_at` (**optional**): [datetime] - Sets the start interval manually. Use with the `no_lock` option.

#### `request_job_exec`

Execute a specified task for a job, often used when a specific task needs to be run without considering the full job lifecycle.

```python
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
    job_interval_started_at: Optional[datetime] = None
) -> None:
```

**Parameters**:

- `job_name`: [str] - A unique identifier for the series of jobs.
- `task`: [Callable]\[[Job], [Awaitable]\[[None]\]\] - Function that defines the task to be executed for the job.
- Other parameters are same as described in `request_job_start`.

## Job Class

The `Job` class encapsulates individual tasks managed and executed by Cronyx.

### Properties

- `id`: [Optional]\[[str]\] - A unique identifier for the job, returns `None` for bypassed job lock.
- `name`: [str] - The identifier for the series of jobs.
- `interval`: [int] - The frequency of the job in milliseconds.
- `is_active`: [bool] - The active status of the job.
- `interval_started_at`: [datetime] - Starting time of the job's interval.
- `interval_ended_at`: [datetime] - Ending time of the job's interval.
- `created_at`: [datetime] - Created date of the job.
- `updated_at`: [datetime] - Last updated date of the job.

### Methods

#### `finish`

Mark a job as successfully completed.

```python
async def finish() -> None:
```

#### `interrupt`

Indicate that a job has been prematurely halted, either due to an error or another unforeseen circumstance.

```python
async def interrupt() -> None:
```

[str]: https://docs.python.org/3/library/string.html "str"
[int]: https://docs.python.org/3/library/functions.html#int "int"
[bool]: https://docs.python.org/3/library/stdtypes.html#boolean-type-bool "bool"
[datetime]: https://docs.python.org/3/library/datetime.html#datetime.datetime "datetime"
[Optional]: https://docs.python.org/3/library/typing.html#typing.Optional "optional"
[List]: https://docs.python.org/3/library/typing.html#typing.List "List"
[Callable]: https://docs.python.org/3/library/typing.html#typing.Callable "Callable"
[Awaitable]: https://docs.python.org/3/library/typing.html#typing.Awaitable "Awaitable"
[Job]: https://github.com/yujiosaka/CronyxClient.py/blob/main/docs/API.md#job-class "Job"
[Union]: https://docs.python.org/3/library/typing.html#typing.Union "Union"
[None]: https://docs.python.org/3/library/constants.html#None "None"
[Duration]: https://date-fns.org/v2.30.0/docs/Duration "Duration"