from contextlib import AbstractContextManager
from typing import Callable

import pandas as pd
from sqlmodel import Session, delete

from sp_editor.models.models import PierLabel


class EtabsPierLabelRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def add(self, params: list):
        """
        Adds a new PierLabel record to the database.

        :param params: List containing [story, label, uniquename, piername].
        :return: The newly added PierLabel object.
        """
        story, label, uniquename, piername = params  # Unpack parameters
        with self.session_factory() as session:
            # Create a new PierLabel instance
            pier_label = PierLabel(
                story=story,
                label=label,
                uniquename=uniquename,
                piername=piername,
            )
            session.add(pier_label)
            session.commit()
            session.refresh(pier_label)
            return pier_label

    def import_pier_labels(self, pier_labels: pd.DataFrame):
        """
        Parses the provided pier labels DataFrame from ETABS and updates the database:
            - Deletes any existing pier label data.
            - Inserts new pier label records from the DataFrame.
        :param pier_labels: DataFrame with pier label data.
        """
        with self.session_factory() as session:
            # Clear existing data using a single DELETE statement
            session.exec(delete(PierLabel))
            session.commit()

            # Prepare PierLabel objects for bulk insertion
            pier_label_objects = [
                PierLabel(
                    story=row["Story"],  # Assuming DataFrame has 'Story' column
                    label=row["Label"],  # Assuming DataFrame has 'Label' column
                    uniquename=row.get("UniqueName"),  # Optional field
                    piername=row.get("PierName"),  # Optional field
                )
                for _, row in pier_labels.iterrows()
            ]

            # Use bulk_save_objects for faster insertions
            session.bulk_save_objects(pier_label_objects)
            session.commit()
