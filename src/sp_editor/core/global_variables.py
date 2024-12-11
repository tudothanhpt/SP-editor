from enum import Enum


class DesignCode(Enum):
    ACI_318_02 = 0
    CSA_A23_3_94 = 1
    ACI_318_05 = 2
    CSA_A23_3_04 = 3
    ACI_318_08 = 4
    ACI_318_11 = 5
    ACI_318_14 = 6
    CSA_A23_3_14 = 7
    ACI_318_19 = 8
    CSA_A23_3_19 = 9

    def __str__(self):
        if self == DesignCode.ACI_318_02:
            return "ACI 318-02"
        elif self == DesignCode.CSA_A23_3_94:
            return "CSA A23.3-94"
        elif self == DesignCode.ACI_318_05:
            return "ACI 318-05"
        elif self == DesignCode.CSA_A23_3_04:
            return "CSA A23.3-04"
        elif self == DesignCode.ACI_318_08:
            return "ACI 318-08"
        elif self == DesignCode.ACI_318_11:
            return "ACI 318-11"
        elif self == DesignCode.ACI_318_14:
            return "ACI 318-14"
        elif self == DesignCode.CSA_A23_3_14:
            return "CSA A23.3-14"
        elif self == DesignCode.ACI_318_19:
            return "ACI 318-19"
        elif self == DesignCode.CSA_A23_3_19:
            return "CSA A23.3-19"

    @classmethod
    def from_string(cls, code_str):
        str_code_map = {
            "ACI 318-02": cls.ACI_318_02,
            "CSA A23.3-94": cls.CSA_A23_3_94,
            "ACI 318-05": cls.ACI_318_05,
            "CSA A23.3-04": cls.CSA_A23_3_04,
            "ACI 318-08": cls.ACI_318_08,
            "ACI 318-11": cls.ACI_318_11,
            "ACI 318-14": cls.ACI_318_14,
            "CSA A23.3-14": cls.CSA_A23_3_14,
            "ACI 318-19": cls.ACI_318_19,
            "CSA A23.3-19": cls.CSA_A23_3_19,
        }
        return str_code_map.get(code_str, None)


class BarGroupType(Enum):
    USER_DEFINED = 0
    ASTM615 = 1
    CSA_G30_18 = 2
    PR_EN_10080 = 3
    ASTM615M = 4

    def __str__(self):
        if self == BarGroupType.USER_DEFINED:
            return "User Defined"
        elif self == BarGroupType.ASTM615:
            return "ASTM615"
        elif self == BarGroupType.CSA_G30_18:
            return "CSA G30.18"
        elif self == BarGroupType.PR_EN_10080:
            return "prEN 10080"
        elif self == BarGroupType.ASTM615M:
            return "ASTM615M"

    @classmethod
    def from_string(cls, type_str):
        str_type_map = {
            "User Defined": cls.USER_DEFINED,
            "ASTM615": cls.ASTM615,
            "CSA G30.18": cls.CSA_G30_18,
            "prEN 10080": cls.PR_EN_10080,
            "ASTM615M": cls.ASTM615M,
        }
        return str_type_map.get(type_str, None)


class UnitSystem(Enum):
    ENGLISH = 0
    METRIC = 1

    def __str__(self):
        if self == UnitSystem.ENGLISH:
            return "English Unit"
        elif self == UnitSystem.METRIC:
            return "Metric Units"

    @classmethod
    def from_string(cls, type_str):
        str_type_map = {
            "English Unit": cls.ENGLISH,
            "Metric Units": cls.METRIC,
        }
        return str_type_map.get(type_str, None)


class SectionCapacityMethod(Enum):
    MOMENT_CAPACITY = 0
    CRITICAL_CAPACITY = 1

    def __str__(self):
        if self == SectionCapacityMethod.MOMENT_CAPACITY:
            return "Moment capacity"
        elif self == SectionCapacityMethod.CRITICAL_CAPACITY:
            return "Critical Capacity"

    @classmethod
    def from_string(cls, type_str):
        str_type_map = {
            "Moment capacity": cls.MOMENT_CAPACITY,
            "Critical Capacity": cls.CRITICAL_CAPACITY,
        }
        return str_type_map.get(type_str, None)


class ConfinementType(Enum):
    TIED = 0
    SPIRAL = 1
    OTHER = 2

    def __str__(self):
        if self == ConfinementType.TIED:
            return "Tied"
        elif self == ConfinementType.SPIRAL:
            return "Spiral"
        elif self == ConfinementType.OTHER:
            return "Other"

    @classmethod
    def from_string(cls, type_str):
        str_type_map = {
            "Tied": cls.TIED,
            "Spiral": cls.SPIRAL,
            "Other": cls.OTHER,
        }
        return str_type_map.get(type_str, None)
