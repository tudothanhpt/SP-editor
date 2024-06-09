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
    diameter: str
    area: str
    weight: str


class LevelGroup(SQLModel, table=True):
    """
    Level group with each level name contain all pier force infor related to that level
    """
    id: int | None = Field(default=None, primary_key=True)
    name: str
    levels: list["PierForce"] = Relationship(back_populates="level")


class PierForce(SQLModel, table=True):
    """
    Store data from etabs input Pier force table
    """
    id: int | None = Field(default=None, primary_key=True)
    story: str = Field(index=True)
    pier: str = Field(index=True)
    load_combo: str
    location: str
    P: str
    V2: str
    V3: str
    T: str
    M2: str
    M3: str

    level_id: int | None = Field(default=None, foreign_key="levelgroup.id")
    level: LevelGroup | None = Relationship(back_populates="levels")

