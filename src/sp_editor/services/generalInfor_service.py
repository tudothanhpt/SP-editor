from typing import List, Type

from sp_editor.models.models import GeneralInfor
from sp_editor.repositories.generalInfor_repository import GeneralInforRepository


class GeneralInforService:
    def __init__(self, generalInfor_repository: GeneralInforRepository):
        self.repository = generalInfor_repository

    def add_generalInfor(self, params: List[str], file_path: str) -> GeneralInfor:
        """
        Add a new GeneralInfor record.

        Args:
            params (List[str]): A list containing the fields for GeneralInfor.
            file_path (str): The file path where the project is stored.

        Returns:
            GeneralInfor: The created GeneralInfor instance.
        """
        return self.repository.add(params, file_path)

    def update_generalInfor(self, params: List[str], file_path: str) -> Type[GeneralInfor] | None:
        """
        Update the GeneralInfor record with the given parameters if there are changes.

        Args:
            params (List[str]): A list containing the updated fields for GeneralInfor.
            file_path (str): The updated file path.

        Returns:
            GeneralInfor: The updated GeneralInfor instance, or None if no update was necessary.
        """
        # Retrieve the current GeneralInfor record
        current_infor = self.repository.get_by_id(1)

        if not current_infor:
            raise ValueError("General information record does not exist.")

        # Compare the current data with the new data
        current_data = [
            current_infor.design_code,
            current_infor.unit_system,
            current_infor.bar_set,
            current_infor.confinement,
            current_infor.section_capacity,
            current_infor.file_path,
        ]

        new_data = params + [file_path]

        if current_data == new_data:
            # No changes detected
            return None

        # Perform the update since changes are detected
        return self.repository.update(params, file_path)

    def get_generalInfor(self, infor_id: int = 1) -> GeneralInfor:
        """
        Retrieve a GeneralInfor record by its ID.

        Args:
            infor_id (int): The ID of the GeneralInfor to retrieve. Default to 1.

        Returns:
            GeneralInfor: The retrieved GeneralInfor instance.
        """
        return self.repository.get_by_id(infor_id)

    def get_file_path(self) -> str | None:
        """
        Retrieve the currently stored file path.

        Returns:
            str | None: The file path if available, otherwise None.
        """
        return self.repository.get_file_path()


