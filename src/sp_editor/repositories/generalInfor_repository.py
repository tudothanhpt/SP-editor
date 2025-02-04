from dependency_injector.wiring import inject
from sqlmodel import Session

from contextlib import AbstractContextManager
from typing import Callable, Type

from sp_editor.models.models import GeneralInfor


class GeneralInforRepository:
    @inject
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def add(self, params: list[str], file_path:str) -> GeneralInfor:
        d_code, u_sys, b_set, confi, s_capacity = params
        with self.session_factory() as session:
            infor = GeneralInfor(
                design_code=d_code,
                unit_system=u_sys,
                bar_set=b_set,
                confinement=confi,
                section_capacity=s_capacity,
                file_path=file_path
            )
            session.add(infor)
            session.commit()
            session.refresh(infor)
            return infor

    def update(self, params: list[str],file_path:str) -> Type[GeneralInfor] | None:
        d_code, u_sys, b_set, confi, s_capacity = params
        with self.session_factory() as session:
            infor = session.get(GeneralInfor, 1)
            infor.design_code = d_code
            infor.unit_system = u_sys
            infor.bar_set = b_set
            infor.confinement = confi
            infor.section_capacity = s_capacity,
            infor.file_path=file_path,

            session.add(infor)
            session.commit()
            session.refresh(infor)
            return infor

    def get_by_id(self, infor_id: int = 1):
        with self.session_factory() as session:
            infor = session.get(GeneralInfor, infor_id)
            return infor

    def get_file_path(self)->str|None:
        "Retrieve the current file path from a generalinfor database"
        with self.session_factory() as session:
            infor = session.get(GeneralInfor, 1)
            return infor.file_path if infor else None
