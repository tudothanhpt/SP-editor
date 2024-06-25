from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from sqlmodel import Session, select
from sp_editor.database.models import GroupLevel, PierLabel, Level, SectionDesignerShape, MaterialConcrete, \
    MaterialRebar, BarSet, CalculationCase, GeneralInfor
from sqlalchemy.engine.base import Engine


def get_current_unit(engine: Engine):
    with Session(engine) as session:
        statement = select(GeneralInfor.unit_system)
        results = session.exec(statement)
        unit = results.one()
        return unit


def get_sds_section_name(engine: Engine):
    with Session(engine) as session:
        statement = select(SectionDesignerShape.sectionName)
        results = session.exec(statement)
        sds_names = results.all()
        return sds_names


def get_concrete_name(engine: Engine):
    with Session(engine) as session:
        statement = select(MaterialConcrete.name)
        results = session.exec(statement)
        concrete_name = results.all()
        return concrete_name


def get_concrete_fc_Ec(engine: Engine, name: str):
    try:
        with Session(engine) as session:
            statement = select(MaterialConcrete.fc, MaterialConcrete.Ec).where(MaterialConcrete.name == name)
            results = session.exec(statement)
            output = results.one()
            fc, Ec = output
            return fc, Ec
    except NoResultFound:
        print(f"No result found for the concrete name: {name}")
        return None, None
    except MultipleResultsFound:
        print(f"Multiple results found for the concrete name: {name}")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


def get_steel_fy_Es(engine: Engine, name: str):
    try:
        with Session(engine) as session:
            statement = select(MaterialRebar.fy, MaterialRebar.Es).where(MaterialRebar.name == name)
            results = session.exec(statement)
            output = results.one()
            fy, Es = output
            return fy, Es
    except NoResultFound:
        print(f"No result found for the steel name: {name}")
        return None, None
    except MultipleResultsFound:
        print(f"Multiple results found for the steel name: {name}")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


def get_steel_name(engine: Engine):
    with Session(engine) as session:
        statement = select(MaterialRebar.name)
        results = session.exec(statement)
        rebar_name = results.all()
        return rebar_name


def get_steel_fy(engine: Engine, name: str):
    with Session(engine) as session:
        statement = select(MaterialRebar.fy).where(MaterialRebar.name == name)
        results = session.exec(statement)
        fy = results.one()
        return fy


def get_rebar_size_name(engine: Engine):
    with Session(engine) as session:
        statement = select(BarSet.size)
        results = session.exec(statement)
        barset_name = results.all()
        return barset_name


def get_rebar_area_from_name(engine: Engine, name: str):
    with Session(engine) as session:
        statement = select(BarSet.area).where(BarSet.size == name)
        results = session.exec(statement)
        barset_area = results.one()
        return barset_area


def create_calculation_case(engine: Engine, params: list[str | float]):
    (tier, is_pier_name, folder, sds, pier, bar_cover, bar_no, bar_area, bar_spacing, concrete_ag, sds_as, rho,
     material_fc, material_fy, material_ec, material_es, from_story, to_story, case_path) = params

    with Session(engine) as session:
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
