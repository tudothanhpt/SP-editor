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


def get_concrete_name_from_properties(engine: Engine, fc: str, ec: str):
    with Session(engine) as session:
        statement = select(MaterialConcrete.name).where(MaterialConcrete.fc == fc).where(MaterialConcrete.Ec == ec)
        result = session.exec(statement)
        concrete_name = result.one()
        return concrete_name


def get_steel_name_from_properties(engine: Engine, fy: str, es: str):
    with Session(engine) as session:
        statement = select(MaterialRebar.name).where(MaterialRebar.fy == fy).where(MaterialRebar.Es == es)
        result = session.exec(statement)
        steel_name = result.one()
        return steel_name


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


def get_calculation_case(engine: Engine, case_id):
    with Session(engine) as session:
        statement = select(CalculationCase).where(CalculationCase.id == case_id)
        results = session.exec(statement)
        case = results.one_or_none()
        if case:
            return case.to_list()
        return None


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


def update_calculation_case(engine: Engine, params: list[str | float], case_id: int):
    (tier, is_pier_name, folder, sds, pier, bar_cover, bar_no, bar_area, bar_spacing, concrete_ag, sds_as, rho,
     material_fc, material_fy, material_ec, material_es, from_story, to_story, case_path) = params

    with Session(engine) as session:
        statement = select(CalculationCase).where(CalculationCase.id == case_id)
        results = session.exec(statement)
        case = results.one()
        
        case.tier = tier
        case.isPierName = is_pier_name
        case.folder = folder
        case.sds = sds
        case.pier = pier
        case.barCover = bar_cover
        case.barNo = bar_no
        case.barArea = bar_area
        case.barSpacing = bar_spacing
        case.concreteAg = concrete_ag
        case.sdsAs = sds_as
        case.rho = rho
        case.materialFc = material_fc
        case.materialFy = material_fy
        case.materialEc = material_ec
        case.materialEs = material_es

        case.fromStory = from_story
        case.toStory = to_story

        case.casePath = case_path
        case.spColumnFile = None

        session.add(case)
        session.commit()
        session.refresh(case)
        return case


def delete_calculation_case(engine: Engine, case_id: int):
    with Session(engine) as session:
        statement = select(CalculationCase).where(CalculationCase.id == case_id)
        results = session.exec(statement)
        case = results.one()
        session.delete(case)
        session.commit()


def update_dcr_by_spcolumnfile(engine: Engine, spColumnFile, new_dcr_value, loadcombo_id):
    with Session(engine) as session:
        statement = select(CalculationCase).where(CalculationCase.spColumnFile == spColumnFile)
        results = session.exec(statement).all()
        print(results)

        for row in results:
            row.dcr = new_dcr_value
            row.forceCombo = loadcombo_id
            session.add(row)

        session.commit()
