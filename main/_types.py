from typing import List, Dict, Any, Optional, Literal
from pydantic import Field
from alt_proc.types import Strict
from datetime import datetime

class User(Strict):
    login: str
    md5: str
    roles: List[str]


class Project(Strict):
    project_id: int
    login: str
    name: str
    start_date: Optional[str]
    end_date: Optional[str]
    border: str

class Meta(Strict):
    project_id: int
    scene_id: str
    date: str
    border: bytes
    filename: str
    xg0: float
    xg1: float
    yg0: float
    yg1: float
