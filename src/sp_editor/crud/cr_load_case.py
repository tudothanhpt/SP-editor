from pandas import DataFrame
from sqlalchemy import func

from sqlmodel import Session, select
from sp_editor.database.models import GroupLevel, PierLabel, Level, SectionDesignerShape

from sqlalchemy.engine.base import Engine


def get_sds_section_name(engine: Engine):
    with Session(engine) as session:
        statement = select(SectionDesignerShape.sectionName)
        results = session.exec(statement)
        sds_names = results.all()
        return sds_names
