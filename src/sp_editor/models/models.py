from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, List


class GeneralInfor(SQLModel, table=True):
    """
    Gather init infor of a spcolumn file
    """

    id: int | None = Field(default=None, primary_key=True)
    design_code: str
    unit_system: str
    bar_set: str
    confinement: str
    section_capacity: str
    file_path: str


class MaterialConcrete(SQLModel, table=True):
    """
    Concrete material properties
    """

    id: Optional[int] = Field(default=None, primary_key=True)
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

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = None
    fy: Optional[float] = None
    Es: Optional[float] = None
    ety: str = Field(default="0.0021")


class BarSet(SQLModel, table=True):
    """
    Bar set material properties
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    size: str
    diameter: float
    area: float
    weight: float


class Level(SQLModel, table=True):
    """Level definition of an Etabs model."""

    id: int | None = Field(default=None, primary_key=True)
    story: str = Field(default=None, unique=True, index=True)
    height: str = Field(default=None)
    tier: str | None = Field(default=None)

    pierlabels: List["PierLabel"] = Relationship(back_populates="level")


class SectionDesignerShape(SQLModel, table=True):
    index: int | None = Field(default=None, primary_key=True)
    sectionType: str = Field(
        default=None,
    )
    sectionName: str = Field(
        default=None,
    )
    shapeName: str = Field(
        default=None,
    )
    x: float = Field(
        default=None,
    )
    y: float = Field(
        default=None,
    )


class PierLabel(SQLModel, table=True):
    index: int | None = Field(default=None, primary_key=True)

    story: str = Field(
        default=None, max_length=50, foreign_key="level.story"
    )  # THIS IS THE KEY CHANGE
    label: str = Field(default=None, max_length=50)
    uniquename: Optional[int] = Field(default=None)
    piername: Optional[str] = Field(default=None, max_length=50)

    pierforces: List["PierForce"] = Relationship(back_populates="pierlabel")
    level: "Level" = Relationship(back_populates="pierlabels")


class PierForce(SQLModel, table=True):
    index: int | None = Field(default=None, primary_key=True)

    pierlabel_index: int = Field(foreign_key="pierlabel.index", index=True)
    pier: str = Field(default=None, max_length=50)
    combo: Optional[str] = Field(default=None, max_length=50)
    location: Optional[str] = Field(default=None)
    p: Optional[float] = Field(default=None)
    v2: Optional[float] = Field(default=None)
    v3: Optional[float] = Field(default=None)
    t: Optional[float] = Field(default=None)
    m2: Optional[float] = Field(default=None)
    m3: Optional[float] = Field(default=None)

    pierlabel: Optional[PierLabel] = Relationship(back_populates="pierforces")


# class GroupLevel(SQLModel, table=True):
#     """
#     GroupLevel model linked to the Level model via a story
#     """
#     id: int | None = Field(default=None, primary_key=True)
#
#     tier: str | None = Field(default=None)
#     story: str = Field(default=None, foreign_key="level.story",index=True)
#
#     level: Optional[Level] = Relationship(back_populates="grouplevels")


class CalculationCase(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tier: str | None = Field(default=None)
    isPierName: bool | None = Field(default=None)
    folder: str | None = Field(default=None)
    sds: str | None = Field(default=None)
    pier: str | None = Field(default=None)

    barCover: float | None = Field(default=None)
    barNo: str | None = Field(default=None)
    barArea: float | None = Field(default=None)
    barSpacing: float | None = Field(default=None)
    concreteAg: float | None = Field(default=None)
    sdsAs: float | None = Field(default=None)
    rho: float | None = Field(default=None)

    materialFc: float | None = Field(default=None)
    materialFy: float | None = Field(default=None)
    materialEc: float | None = Field(default=None)
    materialEs: float | None = Field(default=None)

    fromStory: str | None = Field(default=None)
    toStory: str | None = Field(default=None)

    casePath: str | None = Field(default=None)
    spColumnFile: str | None = Field(default=None)

    forceCombo: str | None = Field(default=None)
    dcr: str | None = Field(default=None)

    def to_list(self):
        return [
            self.id,
            self.tier,
            self.isPierName,
            self.folder,
            self.sds,
            self.pier,
            self.barCover,
            self.barNo,
            self.barArea,
            self.barSpacing,
            self.concreteAg,
            self.sdsAs,
            self.rho,
            self.materialFc,
            self.materialFy,
            self.materialEc,
            self.materialEs,
            self.fromStory,
            self.toStory,
            self.casePath,
            self.spColumnFile,
            self.forceCombo,
            self.dcr,
        ]


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
    Area: Optional[float] = Field(default=None)


class CTISummary(SQLModel, table=True):
    ID2: Optional[str] = Field(default=None, primary_key=True)
    Tier: Optional[str] = Field(default=None)
    Pier: Optional[str] = Field(default=None)
    materialEc: Optional[float] = Field(default=None)
    materialFc: Optional[float] = Field(default=None)
    materialFy: Optional[float] = Field(default=None)
    materialEs: Optional[float] = Field(default=None)
    SDName: Optional[str] = Field(default=None)
    coordinates: Optional[str] = Field(default=None)
    totalBars: Optional[int] = Field(default=None)
    rebarCoordinates: Optional[str] = Field(default=None)
    totalCombos: Optional[int] = Field(default=None)
    filteredForces: Optional[str] = Field(default=None)
    casePath: Optional[str] = Field(default=None)
    pathAfterCreation: Optional[str] = Field(default=None)


class BatchProcessingOutput(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    spColumnFile: str | None = Field(default=None)
    Pu: Optional[float] = Field(default=None)
    Mux: Optional[float] = Field(default=None)
    Muy: Optional[float] = Field(default=None)
    DCR: Optional[float] = Field(default=None)
