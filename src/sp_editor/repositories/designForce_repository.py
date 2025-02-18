from contextlib import AbstractContextManager
from typing import Callable, List

import pandas as pd
from sqlmodel import select, Session, delete
from sqlalchemy.exc import SQLAlchemyError

from sp_editor.models.models import PierForce


class DesignForceRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def add_design_force(self, pier_design_force: pd.DataFrame):
        with self.session_factory() as session:
            try:
                # Clear existing records
                session.exec(delete(PierForce))
                session.commit()

                # Insert new records using bulk insert
                records = pier_design_force.to_dict(orient="records")
                session.bulk_insert_mappings(PierForce, records)
                session.commit()
                print(
                    f"Inserted {len(records)} pier design force successfully."
                )

            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error while creating pier design force: {e}")
