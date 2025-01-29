from typing import List, Callable
from sqlmodel import select, Session
import pandas as pd
from contextlib import AbstractContextManager

from sp_editor.core.find_pier import (
    restructure_sdshapeDF,
    spColumn_CTI_PierPoint,
    shape_area,
)
from sp_editor.models.models import SectionDesignerShape, SDCoordinates_CTI


class EtabsSectionDesignerShapeRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        """
        Initializes the repository with a session factory.
        :param session_factory: A callable that provides a new SQLModel session.
        """
        self.session_factory = session_factory

    def import_section_designer_shapes(self, shapes_df: pd.DataFrame):
        """
        Imports SectionDesignerShape records into the database.
        Deletes existing records and inserts new ones from the DataFrame.

        :param shapes_df: A pandas DataFrame with the following headers:
                          ['sectionType', 'sectionName', 'shapeName', 'x', 'y']
        """
        with self.session_factory() as session:
            # Delete all existing records
            existing_shapes = session.exec(select(SectionDesignerShape)).all()
            if existing_shapes:
                for shape in existing_shapes:
                    session.delete(shape)
                session.commit()

            # Add new records from DataFrame
            for _, row in shapes_df.iterrows():
                shape = SectionDesignerShape(
                    sectionType=row["SectionType"],
                    sectionName=row["SectionName"],
                    shapeName=row["ShapeName"],
                    x=row["X"],
                    y=row["Y"],
                )
                session.add(shape)
            session.commit()

    def get_SDCoordinates_CTI_todb(self):
        """
        Convert Section designer shape from ETABS to CTI format and store in the database.
        """
        with self.session_factory() as session:
            # Fetch data using the repository's get_all method
            df_sd = self.get_all()

            # Restructure data
            lst_PierSDShape = restructure_sdshapeDF(df_sd)
            lst_PierSDName = [
                list(PierSDShape.keys())[0] for PierSDShape in lst_PierSDShape
            ]

            # Compute coordinates and area
            lst_formatted_coordinates_str = []
            lst_area = []

            for SDname in lst_PierSDName:
                formatted_coordinates_str = spColumn_CTI_PierPoint(
                    lst_PierSDShape, SDname
                )
                area = shape_area(lst_PierSDShape, SDname)
                lst_formatted_coordinates_str.append(formatted_coordinates_str)
                lst_area.append(area)

            # Prepare data for insertion
            sd_coordinates_dict_todb = [
                {
                    "SDName": SDname,
                    "Coordinates": formatted_coordinates_str,
                    "Area": area,
                }
                for SDname, formatted_coordinates_str, area in zip(
                    lst_PierSDName, lst_formatted_coordinates_str, lst_area
                )
            ]

            # Delete all existing records using a loop
            existing_shapes = session.exec(select(SDCoordinates_CTI)).all()
            for shape in existing_shapes:
                session.delete(shape)
            session.commit()

            # Insert new data
            for record in sd_coordinates_dict_todb:
                shape = SDCoordinates_CTI(**record)
                session.add(shape)
            session.commit()

    def get_all(self) -> pd.DataFrame:
        """
        Fetch all SectionDesignerShape records and return them as a DataFrame.
        """
        with self.session_factory() as session:
            query = select(SectionDesignerShape)
            results = session.exec(query).all()
            # Convert the ORM objects to a DataFrame
            return pd.DataFrame([record.model_dump() for record in results])

    def get_all_sds(self):
        """
        Get all section designer shape name from database
        :return: Section designer shape
        """
        with self.session_factory() as session:
            return session.exec(select(SectionDesignerShape)).all()

    def get_distinct_section_names(self) -> List[str]:
        """Retrieve distinct section names directly from the database."""
        with self.session_factory() as session:
            result = session.exec(select(SectionDesignerShape.sectionName).distinct()).all()
            return [name for name in result if name]  # Filter out None values

    def add(self, params: list):
        """
        Adds a new SectionDesignerShape record to the database.
        :param params: List containing [sectionType, sectionName, shapeName, x, y].
        :return: The newly added SectionDesignerShape object.
        """
        sectionType, sectionName, shapeName, x, y = params  # Unpack parameters
        with self.session_factory() as session:
            shape = SectionDesignerShape(
                sectionType=sectionType,
                sectionName=sectionName,
                shapeName=shapeName,
                x=x,
                y=y,
            )
            session.add(shape)
            session.commit()
            session.refresh(shape)
            return shape

    def get_by_section_name(self, section_name: str) -> List[SectionDesignerShape]:
        """
        Retrieves SectionDesignerShape records by sectionName.
        :param section_name: The section name to filter by.
        :return: List of SectionDesignerShape objects.
        """
        with self.session_factory() as session:
            statement = select(SectionDesignerShape).where(
                SectionDesignerShape.sectionName == section_name
            )
            return session.exec(statement)

    def delete_by_id(self, shape_id: int):
        """
        Deletes a SectionDesignerShape record by its ID.
        :param shape_id: The ID of the shape to delete.
        """
        with self.session_factory() as session:
            shape = session.get(SectionDesignerShape, shape_id)
            if shape:
                session.delete(shape)
                session.commit()
