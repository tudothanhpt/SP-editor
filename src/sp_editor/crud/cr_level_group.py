import pandas as pd
from pandas import DataFrame
from sqlalchemy import func

from sqlmodel import Session, select
from sp_editor.database.models import GroupLevel, PierLabel, Level

from sqlalchemy.engine.base import Engine

TB_GROUPLEVEL = str(GroupLevel.__name__).lower()


def get_level_to_db(engine: Engine, df: DataFrame):
    df.to_sql("level", con=engine, if_exists="replace")


def get_sds_to_db(engine: Engine, df: DataFrame):
    df.to_sql("sectiondesignershape", con=engine, if_exists="replace")


def get_pier_label_to_db(engine: Engine, df: DataFrame):
    df.to_sql("pierlabel", con=engine, if_exists="replace")


def get_pier_design_force_to_db(engine: Engine, df: DataFrame):
    df.to_sql("pierforce", con=engine, if_exists="replace")


def get_pierlabel_with_level(engine: Engine, stories: list[str]):
    with Session(engine) as session:
        statement = select(PierLabel.piername).where(PierLabel.story.in_(stories))
        result = session.exec(statement)
        piernames = result.all()
        return piernames


def create_level_group(engine: Engine, stories: list[str]):
    id = 0
    with Session(engine) as session:
        for story in stories:
            group = GroupLevel(id=id, story=story, tier="None")
            id += 1
            session.add(group)
        session.commit()


def update_group_level(engine: Engine, stories: list[str], tier_name: str):
    with Session(engine) as session:
        statement = select(GroupLevel).where(GroupLevel.story.in_(stories))
        results = session.exec(statement)
        groups = results.all()
        for group in groups:
            group.tier = tier_name
            session.add(group)
            session.commit()
            session.refresh(group)
        return groups


def return_group_level(engine: Engine, tier_name: list[str]):
    with Session(engine) as session:
        statement = select(GroupLevel)
        results = session.exec(statement)
        groups = results.all()
        for i, group in enumerate(groups):
            group.tier = tier_name[i]
            session.add(group)
            session.commit()
            session.refresh(group)
        return groups


def get_group_level(engine: Engine, empty_tier: bool = False):
    with Session(engine) as session:
        if empty_tier:
            statement = select(GroupLevel.tier).where(GroupLevel.tier != "None")
        else:
            statement = select(GroupLevel.tier)
        results = session.exec(statement)
        groups = results.all()
        return groups


def check_group_level(engine: Engine):
    with Session(engine) as session:
        statement = select(func.count(GroupLevel.story))
        results = session.exec(statement).one()
        return results


def get_level(engine: Engine):
    with Session(engine) as session:
        statement = select(Level.story)
        results = session.exec(statement)
        level_detail = results.all()
        return level_detail


def get_level_from_group(engine: Engine, tier: str):
    with Session(engine) as session:
        statement = select(GroupLevel.id, GroupLevel.story).where(
            GroupLevel.tier == tier
        )
        results = session.exec(statement)
        level_detail = results.all()
        level_detail_sorted = sorted(level_detail, key=lambda x: x.id)
        stories = [
            story for _, story in level_detail_sorted
        ]  # Extract only the story field
        return stories


def read_groupDB(engine):
    # Read SQL table into a DataFrame
    df = pd.read_sql_table(
        table_name=TB_GROUPLEVEL,  # The table to read
        con=engine,  # The SQLAlchemy engine
    )
    df = df.rename(columns={"story": "Story"})
    df = df.rename(columns={"tier": "Tier"})
    print(df)
    return df  # The DataFrame containing the table data


# def update_tier(engine: Engine, list[Level]):
#     with Session(engine) as session:
#         statement = select(Grouplevel).where(Grouplevel.story==)
