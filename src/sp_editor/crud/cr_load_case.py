from pandas import DataFrame
from sqlalchemy import func

from sqlmodel import Session, select
from sp_editor.database.models import GroupLevel, PierLabel, Level, SectionDesignerShape, MaterialConcrete, \
    MaterialRebar, BarSet
from sqlalchemy.engine.base import Engine


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
    with Session(engine) as session:
        statement = select(MaterialConcrete.fc, MaterialConcrete.Ec).where(MaterialConcrete.name == name)
        results = session.exec(statement)
        output = results.one()
        fc, Ec = output
        return fc, Ec


def get_steel_fy_Es(engine: Engine, name: str):
    with Session(engine) as session:
        statement = select(MaterialRebar.fy, MaterialRebar.Es).where(MaterialRebar.name == name)
        results = session.exec(statement)
        output = results.one()
        fy, Es = output
        return fy, Es


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
