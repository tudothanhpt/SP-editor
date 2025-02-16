from contextlib import AbstractContextManager
from typing import Callable, List

import pandas as pd
from sqlmodel import select, Session, delete
from sqlalchemy.exc import SQLAlchemyError

class DesignForceRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

