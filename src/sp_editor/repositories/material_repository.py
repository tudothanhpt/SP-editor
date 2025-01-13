from sqlmodel import Session, select, SQLModel, delete
from contextlib import AbstractContextManager
from typing import Callable, Sequence, Type


class MaterialRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def add(self, model_class: Type[SQLModel], params: dict) -> SQLModel:
        """
        Add a new record to the database.
        :param model_class: SQLModel class to create the instance.
        :param params: Dictionary of field values.
        :return: The created model instance.
        """
        with self.session_factory() as session:
            instance = model_class(**params)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance

    def update(
            self, model_class: Type[SQLModel], id: int, params: dict
    ) -> Type[SQLModel] | None:
        """
        Update an existing record in the database.
        :param model_class: SQLModel class to query the instance.
        :param id: ID of the record to update.
        :param params: Dictionary of updated field values.
        :return: The updated model instance or None if not found.
        """
        with self.session_factory() as session:
            instance = session.get(model_class, id)
            if not instance:
                return None
            for key, value in params.items():
                setattr(instance, key, value)
            session.commit()
            session.refresh(instance)
            return instance

    def delete(self, model_class: Type[SQLModel], id: int) -> Type[SQLModel] | None:
        """
        Delete a record from the database.
        :param model_class: SQLModel class to query the instance.
        :param id: ID of the record to delete.
        :return: The deleted model instance or None if not found.
        """
        with self.session_factory() as session:
            instance = session.get(model_class, id)
            if not instance:
                return None
            session.delete(instance)
            session.commit()
            return instance

    def get_all(self, model_class: Type[SQLModel]) -> Sequence[SQLModel]:
        """
        Retrieve all records of a given type.
        :param model_class: SQLModel class to query.
        :return: A sequence of model instances.
        """
        with self.session_factory() as session:
            return session.exec(select(model_class)).all()

    def import_data(self, model_class: Type[SQLModel], data: list[dict]):
        """
        Import data into the database, replacing existing records.
        :param model_class: SQLModel class to handle.
        :param data: List of dictionaries containing the data.
        """
        with self.session_factory() as session:
            # Delete existing records
            session.exec(delete(model_class))
            session.commit()

            # Insert new records
            for item in data:
                instance = model_class(**item)
                session.add(instance)
            session.commit()
