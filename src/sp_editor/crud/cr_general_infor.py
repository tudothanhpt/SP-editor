from typing import Type

from sqlmodel import Session, select
from sqlalchemy.engine.base import Engine

from database.models import GeneralInfor
from database.database import create_db_and_tables


def create_infor(engine: Engine, params: list[str]) -> GeneralInfor:
    d_code, u_sys, b_set, confi, s_capacity = params
    with Session(engine) as session:
        infor = GeneralInfor(
            design_code=d_code,
            unit_system=u_sys,
            bar_set=b_set,
            confinement=confi,
            section_capacity=s_capacity,
        )
        session.add(infor)
        session.commit()
        session.refresh(infor)
        return infor


def update_infor(engine: Engine, params: list[str]) -> Type[GeneralInfor] | None:
    d_code, u_sys, b_set, confi, s_capacity = params
    with Session(engine) as session:
        infor = session.get(GeneralInfor, 1)
        infor.design_code = d_code
        infor.unit_system = u_sys
        infor.bar_set = b_set
        infor.confinement = confi
        infor.section_capacity = s_capacity

        session.add(infor)
        session.commit()
        session.refresh(infor)
        return infor


def get_infor(engine: Engine) -> Type[GeneralInfor] | None:
    with Session(engine) as session:
        infor = session.get(GeneralInfor, 1)
        return infor
