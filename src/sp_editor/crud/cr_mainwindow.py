import os.path
from typing import List, Any

import pandas as pd
from sqlmodel import Session, select
from sp_editor.database.models import CalculationCase, CTISummary
from sqlalchemy.engine.base import Engine


def update_path_after_creation(engine: Engine):
    with Session(engine) as session:
        statement = select(CTISummary)
        results = session.exec(statement).all()
        for result in results:
            file_name = os.path.basename(result.pathAfterCreation)

            # update table where casePath match
            update_statement = select(CalculationCase).where(
                CalculationCase.casePath == result.casePath
            )
            calculation_entry = session.exec(update_statement).one_or_none()
            if calculation_entry:
                calculation_entry.spColumnFile = file_name
                session.add(calculation_entry)
                session.commit()
                session.refresh(calculation_entry)


# Function to dynamically get column names from the model
def get_column_names(model: Any, attributes: List[str]) -> List[str]:
    model_columns = model.__annotations__.keys()
    return [attr for attr in attributes if attr in model_columns]


# Usage example
desired_columns = [
    CalculationCase.spColumnFile.__str__(),
    CalculationCase.tier.__str__(),
    CalculationCase.fromStory.__str__(),
    CalculationCase.toStory.__str__(),
    CalculationCase.pier.__str__(),
    CalculationCase.materialFc.__str__(),
    CalculationCase.materialFy.__str__(),
    CalculationCase.barNo.__str__(),
    CalculationCase.rho.__str__(),
    CalculationCase.dcr.__str__(),
    CalculationCase.forceCombo.__str__(),
]
column_desired_names = [column.split(".")[1] for column in desired_columns]


def fetch_data_from_db(engine: Engine):
    column_names = get_column_names(CalculationCase, column_desired_names)
    with Session(engine) as session:
        statement = select(*[getattr(CalculationCase, col) for col in column_names])
        results = session.exec(statement)
        cases = results.all()
    # convert into a pandas dataframe
    df = pd.DataFrame(cases, columns=column_names)
    return df
