import json
import os
from typing import Type

import pandas as pd
from sqlmodel import SQLModel

from sp_editor import GLOBALPATH
from sp_editor.models.models import MaterialConcrete
from sp_editor.repositories.material_repository import MaterialRepository


class MaterialService:
    def __init__(self, material_repository: MaterialRepository):
        self.material_repository = material_repository
        self.global_path = GLOBALPATH

    def material_list(self, material: str) -> str | None:
        """
        Return the path to the folder containing JSON files for the given material type.
        :param material: Material type ("concrete" or "rebar").
        :return: Path to the folder or None if invalid.
        """
        material_mapping = {
            "concrete": os.path.join(
                self.global_path,
                "Property Libraries",
                "Materials",
                material.capitalize(),
            ),
            "rebar": os.path.join(
                self.global_path,
                "Property Libraries",
                "Materials",
                material.capitalize(),
            ),
        }
        return material_mapping.get(material)

    def load_material_from_file(self, json_path: str, model_class: Type[SQLModel]):
        """
        Load material data from a JSON file and import it into the database.
        """
        if not json_path or not os.path.exists(json_path):
            raise FileNotFoundError(f"JSON path does not exist: {json_path}")

        try:
            with open(json_path, "r") as f:
                material_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {json_path}. Error: {e}")

        prepared_data = self.prepare_material_data(material_data, model_class)
        self.material_repository.import_data(model_class, prepared_data)

    def prepare_material_data(
        self, material_data: list[dict], model_class: Type[SQLModel]
    ) -> list[dict]:
        """
        Prepare the material data for the repository functions.
        :param material_data: List of material data dictionaries.
        :param model_class: SQLModel class to define the structure.
        :return: Prepared list of material data dictionaries.
        """
        # Define mapping based on the model class
        field_mapping = {
            "MaterialConcrete": ["name", "fc", "Ec", "max_fc", "beta_1", "eu"],
            "MaterialRebar": ["name", "fy", "Es", "ety"],
        }

        class_name = model_class.__name__
        fields = field_mapping.get(class_name, [])

        # Prepare data
        prepared_data = [
            {field: item.get(field, None) for field in fields} for item in material_data
        ]

        return prepared_data

    def add_material(self, model_class: Type[SQLModel], params: dict):
        """
        Add a new material.
        :param model_class: SQLModel class for the material.
        :param params: Dictionary of material properties.
        :return: The added material instance.
        """
        return self.material_repository.add(model_class, params)

    def update_material(self, model_class: Type[SQLModel], id: int, params: dict):
        """
        Update an existing material.
        :param model_class: SQLModel class for the material.
        :param id: ID of the material to update.
        :param params: Dictionary of updated material properties.
        :return: The updated material instance.
        """
        return self.material_repository.update(model_class, id, params)

    def delete_material(self, model_class: Type[SQLModel], id: int):
        """
        Delete an existing material.
        :param model_class: SQLModel class for the material.
        :param id: ID of the material to delete.
        :return: The deleted material instance.
        """
        return self.material_repository.delete(model_class, id)

    def get_all_materials(self, model_class: Type[SQLModel]) -> pd.DataFrame:
        """
        Retrieve all materials of a given type.
        :param model_class: SQLModel class for the material.
        :return: A DataFrame of all materials.
        """
        materials = self.material_repository.get_all(model_class)
        material_df = pd.DataFrame([material.dict() for material in materials])

        # Filter and order the column based on model_class
        if model_class is MaterialConcrete:
            column_to_include = ["name", "fc", "Ec", "max_fc", "beta_1", "eu"]
            filtered_df = material_df[column_to_include]
        else:
            column_to_include = ["name", "fy", "Es", "ety"]
            filtered_df = material_df[column_to_include]

        return filtered_df
