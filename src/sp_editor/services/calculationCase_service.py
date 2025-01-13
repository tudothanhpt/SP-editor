from typing import Type
from sqlmodel import SQLModel
from sp_editor.repositories.barSet_repository import BarsetRepository
from sp_editor.repositories.calculationCase_repository import CalculationCaseRepository
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
        calculationCase_repository: CalculationCaseRepository,
    ):
        self.generalInfor_repository = generalInfor_repository
        self.etabsStory_repository = etabsStory_repository
        self.etabSectionDesignerShape_repository = etabsSectionDesignerShape_repository
        self.material_repository = material_repository
        self.barset_repository = barset_repository
        self.calculationCase_repository = calculationCase_repository

    def get_current_unit(self):
        try:
            result = self.generalInfor_repository.get_by_id(1)
            if not result:
                raise ValueError("General information with ID 1 not found.")
            return result.unit_system
        except Exception as e:
            raise RuntimeError(f"Error fetching current unit: {e}")

    def get_sds_section(self):
        try:
            return self.etabSectionDesignerShape_repository.get_all_sds()
        except Exception as e:
            raise RuntimeError(f"Error fetching SDS sections: {e}")

    def get_material(self, model_class: Type[SQLModel]):
        try:
            return self.material_repository.get_all(model_class)
        except Exception as e:
            raise RuntimeError(f"Error fetching materials: {e}")

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
