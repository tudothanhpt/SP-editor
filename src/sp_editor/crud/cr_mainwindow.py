import os.path

from sqlmodel import Session, select
from sp_editor.database.models import GroupLevel, PierLabel, Level, SectionDesignerShape, MaterialConcrete, \
    MaterialRebar, BarSet, CalculationCase, GeneralInfor, CTISummary
from sqlalchemy.engine.base import Engine


def update_path_after_creation(engine: Engine):
    # id_name = f"{tier}_{pier}"
    # with (Session(engine) as session):
    #     statement1 = select(CTISummary.pathAfterCreation).where(CTISummary.ID2 == id_name)
    #     statement2 = select(CalculationCase).where(CalculationCase.tier == tier).where(
    #         CalculationCase.pier == pier)
    #     result1 = session.exec(statement1)
    #     path_after_create = result1.one()
    #     file_name_after = os.path.basename(path_after_create)
    #
    #     result2 = session.exec(statement2)
    #     calculation_case = result2.one()
    #     calculation_case.spColumnFile = file_name_after
    #     session.add(calculation_case)
    #     session.commit()
    #     session.refresh(calculation_case)
    with Session(engine) as session:
        statement = select(CTISummary)
        results = session.exec(statement).all()
        for result in results:
            file_name = result.casePath.split("\\")[-1]

            # update table where casePath match
            update_statement = select(CalculationCase).where(CalculationCase.casePath == result.casePath)
            calculation_entry = session.exec(update_statement).one_or_none()
            if calculation_entry:
                calculation_entry.spColumnFile = file_name
                session.add(calculation_entry)
                session.commit()
                session.refresh(calculation_entry)
