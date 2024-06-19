from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, List, Dict, Any


class GeneralInfor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    design_code: str
    unit_system: str
    bar_set: str
    confinement: str
    section_capacity: str


class MaterialConcrete(SQLModel, table=True):
    """
    Concrete material properties
    """
    id: int | None = Field(default=None, primary_key=True)
    name: Optional[str] = None
    fc: Optional[float] = None
    Ec: Optional[float] = None
    max_fc: Optional[float] = None
    beta_1: Optional[float] = None
    eu: Optional[float] = None


class MaterialRebar(SQLModel, table=True):
    """
    Steel material properties
    """
    id: int | None = Field(default=None, primary_key=True)
    name: Optional[str] = None
    fy: Optional[float] = None
    Es: Optional[float] = None
    ety: str = Field(default="0.0021")


class BarSet(SQLModel, table=True):
    """
    Bar set material properties
    """
    id: int | None = Field(default=None, primary_key=True)
    size: str
    diameter: float
    area: float
    weight: float


class Level(SQLModel, table=True):
    index: int | None = Field(default=None, primary_key=True)
    story: str = Field(default=None, primary_key=True)
    height: str = Field(default=None)


class SectionDesignerShape(SQLModel, table=True):
    index: int | None = Field(default=None, primary_key=True)
    sectionType: str = Field(default=None, primary_key=True)
    sectionName: str = Field(default=None, primary_key=True)
    shapeName: str = Field(default=None, primary_key=True)
    x: float = Field(default=None, primary_key=True)
    y: float = Field(default=None, primary_key=True)


class PierLabel(SQLModel, table=True):
    index: int | None = Field(default=None, primary_key=True)

    story: str = Field(default=None, primary_key=True, max_length=50)
    label: str = Field(default=None, primary_key=True, max_length=50)
    uniquename: Optional[int] = Field(default=None)
    piername: Optional[str] = Field(default=None, max_length=50)

    pierforces: List["PierForce"] = Relationship(back_populates="pierlabel")
    grouplevels: List["GroupLevel"] = Relationship(back_populates="pierlabel")


class PierForce(SQLModel, table=True):
    index: int | None = Field(default=None, primary_key=True)

    story: str = Field(default=None, foreign_key="pierlabel.story", primary_key=True, max_length=50)
    pier: str = Field(default=None, primary_key=True, max_length=50)
    combo: Optional[str] = Field(default=None, max_length=50)
    location: Optional[str] = Field(default=None, max_length=50)
    p: Optional[float] = Field(default=None)
    v2: Optional[float] = Field(default=None)
    v3: Optional[float] = Field(default=None)
    t: Optional[float] = Field(default=None)
    m2: Optional[float] = Field(default=None)
    m3: Optional[float] = Field(default=None)

    pierlabel: PierLabel = Relationship(back_populates="pierforces")


class GroupLevel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    tier: str | None = Field(default=None, primary_key=True)
    story: str = Field(default=None, foreign_key="pierlabel.story", primary_key=True, max_length=50)

    pierlabel: PierLabel = Relationship(back_populates="grouplevels")


class LoadCombinationsSelection(SQLModel, table=True):
    """
    Bar set material properties
    """
    id: int | None = Field(default=None, primary_key=True)
    allloadCombos: Optional[str] = Field(default=None)
    selectedLoadCombos: Optional[str] = Field(default=None)


class LoadCombinations(SQLModel, table=True):
    """
    Bar set material properties
    """
    id: int | None = Field(default=None, primary_key=True)
    uniqueloadCombos: Optional[str] = Field(default=None)
    
class SDCoordinates_CTI(SQLModel, table=True):
    """
    Bar set material properties
    """
    id: int | None = Field(default=None, primary_key=True)
    SDName: Optional[str] = Field(default=None)
    Coordinates: Optional[str] = Field(default=None)
    
