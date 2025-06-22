from __future__ import annotations
from datetime import datetime
from odmantic import Field

from odmantic import Model


def datetime_now_sec():
    return datetime.now().replace(microsecond=0)


class User(Model):
    __collection__ = "users"
    
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
    matrix_id: str
    full_name: str = Field(default="")
    tests: dict
    medical_history: dict
