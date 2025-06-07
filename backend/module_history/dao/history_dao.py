# -*- coding:utf-8 -*-

from typing import List
from datetime import datetime, time
from module_admin.entity.do.role_do import SysRoleDept
from sqlalchemy import and_, delete, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_gen.constants.gen_constants import GenConstants

from module_history.entity.do.history_do import History
from module_history.entity.vo.history_vo import HistoryPageModel, HistoryModel
from utils.page_util import PageUtil, PageResponseModel


class HistoryDao:


    @classmethod
    async def get_vue_count(cls, db: AsyncSession,type:str,id:int) -> int:
        match type:
            case '0':
                query = select(func.count()).where(History.del_flag == '0',History.predlabel == '0')  # 过滤掉已删除项
            case '1':
                query = select(func.count()).where(History.del_flag == '0',History.predlabel == '1')  # 过滤掉已删除项
            case '2':
                query = select(func.count()).where(History.del_flag == '0',History.predlabel == '2')  # 过滤掉已删除项
            case '3':
                query = select(func.count()).where(History.del_flag == '0',History.predlabel == '3')  # 过滤掉已删除项
            case '4':
                query = select(func.count()).where(History.del_flag == '0',History.predlabel == '4')  # 过滤掉已删除项
            case 'all':
                query = select(func.count()).where(History.del_flag == '0')  # 过滤掉已删除项
            case 'current':
                query = select(func.count()).where(History.del_flag == '0',History.reportid == id)  # 过滤掉已删除项
            case _:
                return 0
        # query = select(func.count()).where(History.del_flag == '0')  # 过滤掉已删除项
        result = await db.execute(query)
        count = result.scalar()  # 获取查询结果中的单一值，即未删除项的数量
        return count




    @classmethod
    async def get_active_count(cls, db: AsyncSession) -> int:
        query = select(func.count()).where(History.del_flag == '0')  # 过滤掉已删除项
        result = await db.execute(query)
        count = result.scalar()  # 获取查询结果中的单一值，即未删除项的数量
        return count


    @classmethod
    async def get_by_id(cls, db: AsyncSession, history_id: int) -> History:
        """根据主键获取单条记录"""
        history = (((await db.execute(
                            select(History)
                            .where(History.id == history_id)))
                       .scalars())
                       .first())
        return history

    """
    查询
    """
    @classmethod
    async def get_history_list(cls, db: AsyncSession,
                             query_object: HistoryPageModel,
                             data_scope_sql: str = None,
                             is_page: bool = False) -> [list | PageResponseModel]:

        query = (
            select(History)
            .where(
                History.id == query_object.id if query_object.id else True,
                # History.location == query_object.location if query_object.location else True,
                History.location.like(f"%{query_object.location}%") if query_object.location else True,
                History.predclass == query_object.predclass if query_object.predclass else True,
                History.predlabel == query_object.predlabel if query_object.predlabel else True,
                History.predscore == query_object.predscore if query_object.predscore else True,
                History.reportid == query_object.reportid if query_object.reportid else True,
                History.del_flag == '0',
                eval(data_scope_sql) if data_scope_sql else True,
            )
            .order_by(desc(History.id))
            # .distinct()
        )
        history_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return history_list

    """
    查询
    """
    @classmethod
    async def android_get_history_list(cls, db: AsyncSession,
                             query_object: HistoryPageModel,
                             is_page: bool = False) -> [list | PageResponseModel]:

        query = (
            select(History)
            .where(
                History.id == query_object.id if query_object.id else True,
                History.location == query_object.location if query_object.location else True,
                History.predclass == query_object.predclass if query_object.predclass else True,
                History.predscore == query_object.predscore if query_object.predscore else True,
                History.reportid == query_object.reportid if query_object.reportid else True,
                History.del_flag == '0',
            )
            .order_by(desc(History.id))
            .distinct()
        )
        history_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return history_list



    @classmethod
    async def add_history(cls, db: AsyncSession, add_model: HistoryModel, auto_commit: bool = True) -> History:
        """
        增加
        """
        history =  History(**add_model.model_dump(exclude_unset=True))
        db.add(history)
        await db.flush()
        if auto_commit:
            await db.commit()
        return history

    @classmethod
    async def edit_history(cls, db: AsyncSession, edit_model: HistoryModel, auto_commit: bool = True) -> History:
        """
        修改
        """
        edit_dict_data = edit_model.model_dump(exclude_unset=True, exclude={*GenConstants.DAO_COLUMN_NOT_EDIT})
        await db.execute(update(History), [edit_dict_data])
        await db.flush()
        if auto_commit:
            await db.commit()
        return await cls.get_by_id(db, edit_model.id)

    @classmethod
    async def del_history(cls, db: AsyncSession, history_ids: List[str], soft_del: bool = True, auto_commit: bool = True):
        """
        删除
        """
        if soft_del:
            await db.execute(update(History).where(History.id.in_(history_ids)).values(del_flag='2'))
        else:
            await db.execute(delete(History).where(History.id.in_(history_ids)))
        await db.flush()
        if auto_commit:
            await db.commit()