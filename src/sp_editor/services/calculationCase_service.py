from typing import Type, Optional, Tuple, List
from sqlmodel import SQLModel

from sp_editor.models.models import MaterialConcrete, MaterialRebar
from sp_editor.repositories.barSet_repository import BarsetRepository
from sp_editor.repositories.calculationCase_repository import CalculationCaseRepository
from sp_editor.repositories.etabsPierLabel_repository import EtabsPierLabelRepository
from sp_editor.repositories.etabsSectionDesignerShape_repository import EtabsSectionDesignerShapeRepository
from sp_editor.repositories.etabsStory_repository import EtabsStoryRepository
from sp_editor.repositories.generalInfor_repository import GeneralInforRepository
from sp_editor.repositories.material_repository import MaterialRepository


class CalculationCaseService:
    def __init__(
            self,
            generalInfor_repository: GeneralInforRepository,
            etabsStory_repository: EtabsStoryRepository,
            etabsSectionDesignerShape_repository: EtabsSectionDesignerShapeRepository,
            material_repository: MaterialRepository,
            barset_repository: BarsetRepository,
            etabsPierLabel_repository: EtabsPierLabelRepository,
            calculationCase_repository: CalculationCaseRepository,
    ):
        self.generalInfor_repository = generalInfor_repository
        self.etabsStory_repository = etabsStory_repository
        self.etabSectionDesignerShape_repository = etabsSectionDesignerShape_repository
        self.material_repository = material_repository
        self.barset_repository = barset_repository
        self.etabsPierLabel_repository = etabsPierLabel_repository
        self.calculationCase_repository = calculationCase_repository

    def get_current_unit(self):
        try:
            result = self.generalInfor_repository.get_by_id(1)
            if not result:
                raise ValueError("General information with ID 1 not found.")
            return result.unit_system
        except Exception as e:
            raise RuntimeError(f"Error fetching current unit: {e}")

    def get_all_sds_sections(self):
        try:
            return self.etabSectionDesignerShape_repository.get_distinct_section_names()
        except Exception as e:
            raise RuntimeError(f"Error fetching SDS sections: {e}")

    def get_all_material_names(self):
        try:
            """
                Retrieve a list of all material names from both Concrete and Rebar tables.
                :return: List of material names.
                """
            concrete_materials = self.material_repository.get_all(MaterialConcrete)
            rebar_materials = self.material_repository.get_all(MaterialRebar)

            concrete_names = [mat.name for mat in concrete_materials if mat.name]
            rebar_names = [mat.name for mat in rebar_materials if mat.name]

            return concrete_names, rebar_names
        except Exception as e:
            raise RuntimeError(f"Error fetching materials: {e}")

    def get_concrete_properties(self, concrete_name: str) -> Optional[Tuple[float, float]]:
        """
        Retrieve concrete properties (fc, Ec) by name.

        :param concrete_name: The name of the concrete material.
        :return: A tuple (fc, Ec) or None if not found.
        """
        try:
            concrete = self.material_repository.get_by_name(MaterialConcrete, concrete_name)
            if concrete:
                return concrete.fc, concrete.Ec
            return None
        except Exception as e:
            raise RuntimeError(f"Error fetching concrete properties: {e}")

    def get_steel_properties(self, steel_name: str) -> Optional[Tuple[float, float]]:
        """
        Retrieve steel properties (fy, Es) by name.

        :param steel_name: The name of the steel material.
        :return: A tuple (fy, Es) or None if not found.
        """
        try:
            steel = self.material_repository.get_by_name(MaterialRebar, steel_name)
            if steel:
                return steel.fy, steel.Es
            return None
        except Exception as e:
            raise RuntimeError(f"Error fetching steel properties: {e}")

    def get_rebar_size_name(self):
        try:
            return self.barset_repository.get_all_barset_name()
        except Exception as e:
            raise RuntimeError(f"Error fetching rebar size names: {e}")

    def get_rebar_area_by_size(self, bar_size: str):
        try:
            result = self.barset_repository.get_by_size(bar_size)
            if not result:
                raise ValueError(f"No rebar found with size {bar_size}.")
            return result
        except Exception as e:
            raise RuntimeError(f"Error fetching rebar area for size {bar_size}: {e}")

    def get_unique_pier_names_by_tier(self, tier_name: str) -> List[str]:
        """get list of unique pier label name based on tier name"""
        return self.etabsPierLabel_repository.get_unique_pier_names_by_tier(tier_name)

    def get_SDS_properties(self, param):
        # TODO: get properties from section designer shape ( Ag, As, rho)
        pass

    def create_calculation_case(self, params):
        try:
            return self.calculationCase_repository.add(params)
        except Exception as e:
            raise RuntimeError(f"Error creating CalculationCase: {e}")

    def get_calculation_case_by_id(self, case_id: int):
        try:
            return self.calculationCase_repository.get_by_id(case_id)
        except Exception as e:
            raise RuntimeError(f"Error fetching CalculationCase with ID {case_id}: {e}")

    def get_all_calculation_cases(self):
        try:
            return self.calculationCase_repository.get_all()
        except Exception as e:
            raise RuntimeError(f"Error fetching all CalculationCases: {e}")

    def update_calculation_case(self, case_id: int, updates: dict):
        try:
            return self.calculationCase_repository.update(case_id, updates)
        except Exception as e:
            raise RuntimeError(f"Error updating CalculationCase with ID {case_id}: {e}")

    def delete_calculation_case(self, case_id: int):
        try:
            return self.calculationCase_repository.delete(case_id)
        except Exception as e:
            raise RuntimeError(f"Error deleting CalculationCase with ID {case_id}: {e}")
