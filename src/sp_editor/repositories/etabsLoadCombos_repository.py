from contextlib import AbstractContextManager
from typing import Callable, List

import pandas as pd
from sqlmodel import select, Session, delete
from sqlalchemy.exc import SQLAlchemyError

from sp_editor.models.models import LoadCombinations, LoadCombinationsSelection


class EtabsLoadCombosRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def create_load_combos(self, df: pd.DataFrame):
        """
        Insert or replace the LoadCombinations table with data from the DataFrame.
        """
        with self.session_factory() as session:
            try:
                # Clear existing records
                session.exec(delete(LoadCombinations))
                session.commit()

                # Insert new records using bulk insert
                records = df.to_dict(orient="records")
                session.bulk_insert_mappings(LoadCombinations, records)
                session.commit()
                print(f"Inserted {len(records)} load combinations successfully.")

            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error while creating load combinations: {e}")

    def create_load_combo_selections(self, df: pd.DataFrame):
        """
        Insert or replace the LoadCombinationsSelection table with data from the DataFrame.
        """
        with self.session_factory() as session:
            try:
                # Clear existing records
                session.exec(delete(LoadCombinationsSelection))
                session.commit()

                # Insert new records using bulk insert
                records = df.to_dict(orient="records")
                session.bulk_insert_mappings(LoadCombinationsSelection, records)
                session.commit()
                print(
                    f"Inserted {len(records)} load combination selections successfully."
                )

            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error while creating load combination selections: {e}")

    def get_all_load_combos(self) -> pd.DataFrame:
        """
        Retrieve all unique load combinations as a DataFrame.

        :return: DataFrame containing all load combinations.
        """
        with self.session_factory() as session:
            try:
                combos = session.exec(select(LoadCombinations)).all()
                return pd.DataFrame([combo.model_dump() for combo in combos])
            except SQLAlchemyError as e:
                print(f"Error while retrieving load combinations: {e}")
                return pd.DataFrame()

    def get_all_load_combo_selections(self) -> pd.DataFrame:
        """
        Retrieve all load combination selections as a DataFrame.

        :return: DataFrame containing all load combination selections.
        """
        with self.session_factory() as session:
            try:
                selections = session.exec(select(LoadCombinationsSelection)).all()
                return pd.DataFrame(
                    [selection.model_dump() for selection in selections]
                )
            except SQLAlchemyError as e:
                print(f"Error while retrieving load combination selections: {e}")
                return pd.DataFrame()

    def update_combo_selections(self, data: List[dict]) -> None:
        """
        Writes the updated load combination selection data back to the database.

        :param data: List of dictionaries representing load combination selection records.
        """
        with self.session_factory() as session:
            try:
                # Clear existing records in the table
                session.exec(delete(LoadCombinationsSelection))
                session.commit()

                # Bulk insert new records
                session.bulk_insert_mappings(LoadCombinationsSelection, data)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise RuntimeError(f"Error while updating load combination selections: {e}")