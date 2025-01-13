from contextlib import AbstractContextManager
from typing import Callable, Optional, List, Sequence, Any
from sqlmodel import select, Session
from sqlmodel.exc import SQLAlchemyError
from sp_editor.models.models import CalculationCase


class CalculationCaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def add(self, params: List) -> CalculationCase:
        try:
            (
                tier, is_pier_name, folder, sds, pier, bar_cover, bar_no, bar_area, bar_spacing, concrete_ag, sds_as,
                rho,
                material_fc, material_fy, material_ec, material_es, from_story, to_story, case_path
            ) = params

            with self.session_factory() as session:
                calculation_case = CalculationCase(
                    tier=tier,
                    isPierName=is_pier_name,
                    folder=folder,
                    sds=sds,
                    pier=pier,
                    barCover=bar_cover,
                    barNo=bar_no,
                    barArea=bar_area,
                    barSpacing=bar_spacing,
                    concreteAg=concrete_ag,
                    sdsAs=sds_as,
                    rho=rho,
                    materialFc=material_fc,
                    materialFy=material_fy,
                    materialEc=material_ec,
                    materialEs=material_es,
                    fromStory=from_story,
                    toStory=to_story,
                    casePath=case_path,
                    spColumnFile=None
                )

                session.add(calculation_case)
                session.commit()
                session.refresh(calculation_case)
                return calculation_case
        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to add CalculationCase: {e}")

    def get_by_id(self, case_id: int) -> Optional[CalculationCase]:
        try:
            with self.session_factory() as session:
                statement = select(CalculationCase).where(CalculationCase.id == case_id)
                result = session.exec(statement).first()
                if not result:
                    raise ValueError(f"CalculationCase with ID {case_id} not found.")
                return result
        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to retrieve CalculationCase with ID {case_id}: {e}")

    def get_all(self) -> Sequence[CalculationCase]:
        try:
            with self.session_factory() as session:
                statement = select(CalculationCase)
                results = session.exec(statement).all()
                return results
        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to retrieve all CalculationCase records: {e}")

    def update(self, case_id: int, updates: dict) -> Optional[CalculationCase]:
        """
        Updates a CalculationCase record with the provided data.
        :param case_id: The ID of the CalculationCase to update.
        :param updates: A dictionary of fields to update and their new values.
        :return: The updated CalculationCase instance or None if not found or an error occurs.
        """
        try:
            with self.session_factory() as session:
                statement = select(CalculationCase).where(CalculationCase.id == case_id)
                calculation_case = session.exec(statement).first()

                if not calculation_case:
                    return None

                for key, value in updates.items():
                    if hasattr(calculation_case, key):
                        setattr(calculation_case, key, value)

                session.add(calculation_case)
                session.commit()
                session.refresh(calculation_case)
                return calculation_case
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error updating CalculationCase with ID {case_id}: {e}")

    def delete(self, case_id: int) -> bool:
        """
        Deletes a CalculationCase record by its ID.
        :param case_id: The ID of the CalculationCase to delete.
        :return: True if the record was successfully deleted, False otherwise.
        """
        try:
            with self.session_factory() as session:
                statement = select(CalculationCase).where(CalculationCase.id == case_id)
                calculation_case = session.exec(statement).first()

                if not calculation_case:
                    return False

                session.delete(calculation_case)
                session.commit()
                return True
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error deleting CalculationCase with ID {case_id}: {e}")

    def filter_by_field(self, field_name: str, value: Any) -> Sequence[CalculationCase]:
        """
        Filters CalculationCase records by a specific field and value.
        :param field_name: The name of the field to filter by.
        :param value: The value to match.
        :return: A list of matching CalculationCase instances or an empty list if an error occurs.
        :raises AttributeError: If the specified field does not exist in the CalculationCase model.
        """
        try:
            with self.session_factory() as session:
                if not hasattr(CalculationCase, field_name):
                    raise AttributeError(f"CalculationCase has no field named '{field_name}'")

                statement = select(CalculationCase).where(getattr(CalculationCase, field_name) == value)
                results = session.exec(statement).all()
                return results
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error filtering CalculationCase records by {field_name} = {value}: {e}")

    def get_count(self) -> int:
        """
        Retrieves the total count of CalculationCase records.
        :return: The count of CalculationCase records or 0 if an error occurs.
        """
        try:
            with self.session_factory() as session:
                statement = select(CalculationCase)
                count = len(session.exec(statement).all())
                return count
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error retrieving count of CalculationCase records: {e}")
