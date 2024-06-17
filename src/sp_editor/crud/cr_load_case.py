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


def get_steel_name(engine: Engine):
    with Session(engine) as session:
        statement = select(MaterialRebar.name)
        results = session.exec(statement)
        rebar_name = results.all()
        return rebar_name


def get_rebar_size_name(engine: Engine):
    with Session(engine) as session:
        statement = select(BarSet.size)
        results = session.exec(statement)
        barset_name = results.all()
        return barset_name
