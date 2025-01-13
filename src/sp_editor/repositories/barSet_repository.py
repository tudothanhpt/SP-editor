import pandas as pd
from sqlmodel import Session, select
from contextlib import AbstractContextManager
from typing import Callable, Optional, Type, List

from sp_editor.models.models import BarSet


class BarsetRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def add(self, params: list):
        size, diameter, area, weight = params
        with self.session_factory() as session:
            bar_set = BarSet(size=size, diameter=diameter, area=area, weight=weight)
            session.add(bar_set)
            session.commit()
            session.refresh(bar_set)
            return bar_set

    def update(self, bar_id: int, params: list) -> Type[BarSet] | None:
        size, diameter, area, weight = params
        with self.session_factory() as session:
            bar_set = session.get(BarSet, bar_id)
            if not bar_set:
                return None

            bar_set.size = size
            bar_set.diameter = diameter
            bar_set.area = area
            bar_set.weight = weight

            session.add(bar_set)
            session.commit()
            session.refresh(bar_set)
            return bar_set

    def get_by_id(self, bar_id: int) -> Optional[BarSet]:
        """
        Get barset by id
        :param bar_id:
        """
        with self.session_factory() as session:
            bar_set = session.get(BarSet, bar_id)
            return bar_set

    def get_by_size(self, bar_size: str) -> Optional[BarSet]:
        """
        Get barset area by size
        :param bar_size: str
        """
        with self.session_factory() as session:
            stmt = select(BarSet).where(BarSet.size == bar_size)
            return session.exec(stmt).one()

    def get_all_barset_name(self) -> list[BarSet.size]:
        """
        Get all barset names and return them as a list
        """
        with self.session_factory() as session:
            # Fetch all records from the database
            results = session.exec(select(BarSet)).all()
            # return a list of barset name
            barset_name: list[str] = [barset.size for barset in results]

            return barset_name

    def get_all(self) -> pd.DataFrame:
        """
        Fetches all records of `BarSet` and returns them as a pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing all BarSet records.
        """
        with self.session_factory() as session:
            # Fetch all records from the database
            results = session.exec(select(BarSet)).all()

            # Convert results to a pandas DataFrame
            data = [row.dict() for row in results]
            return pd.DataFrame(data)

    def delete_by_id(self, bar_id: int) -> bool:
        with self.session_factory() as session:
            bar_set = session.get(BarSet, bar_id)
            if not bar_set:
                return False

            session.delete(bar_set)
            session.commit()
            return True

    def import_barsets(self, barsets_data: list[dict]):
        """
        Parses the provided barsets data and updates the database:
        - Deletes any existing BarSet data.
        - Inserts new BarSet records.
        """
        with self.session_factory() as session:
            # Check for existing data
            existing_barsets = session.exec(select(BarSet)).all()

            # If data exists, delete all records
            if existing_barsets:
                for barset in existing_barsets:
                    session.delete(barset)
                session.commit()

            # Add new records
            for item in barsets_data:
                bar_set = BarSet(**item)
                session.add(bar_set)

            # Commit the changes
            session.commit()
