from typing import Optional, TypedDict


class Credentials(TypedDict):
    username: str
    password: str


class Duration(TypedDict):
    years: Optional[int]
    months: Optional[int]
    weeks: Optional[int]
    days: Optional[int]
    hours: Optional[int]
    minutes: Optional[int]
    seconds: Optional[int]
