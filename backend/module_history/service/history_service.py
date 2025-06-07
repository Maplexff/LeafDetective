# -*- coding:utf-8 -*-

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.common_util import CamelCaseUtil, export_list2excel
from module_admin.entity.vo.sys_table_vo import SysTablePageModel
from module_admin.service.sys_table_service import SysTableService
from utils.page_util import PageResponseModel
from module_history.dao.history_dao import HistoryDao
from module_history.entity.do.history_do import History
from module_history.entity.vo.history_vo import HistoryPageModel, HistoryModel


class HistoryService:
    """
    用户管理模块服务层
    """

    @classmethod
    async def get_history_list(cls, query_db: AsyncSession, query_object: HistoryPageModel, data_scope_sql: str) -> [list | PageResponseModel]:
        history_list = await HistoryDao.get_history_list(query_db, query_object, data_scope_sql, is_page=True)
        return history_list

    @classmethod
    async def get_history_by_id(cls, query_db: AsyncSession, history_id: int) -> HistoryModel:
        history = await  HistoryDao.get_by_id(query_db, history_id)
        history_model = HistoryModel(**CamelCaseUtil.transform_result(history))
        return history_model


    @classmethod
    async def add_history(cls, query_db: AsyncSession, query_object: HistoryModel) -> HistoryModel:
        history = await HistoryDao.add_history(query_db, query_object)
        history_model = HistoryModel(**CamelCaseUtil.transform_result(history))
        return history_model


    @classmethod
    async def update_history(cls, query_db: AsyncSession, query_object: HistoryModel) -> HistoryModel:
        history = await HistoryDao.edit_history(query_db, query_object)
        history_model = HistoryModel(**CamelCaseUtil.transform_result(history))
        return history_model


    @classmethod
    async def del_history(cls, query_db: AsyncSession, history_ids: List[str]):
        await HistoryDao.del_history(query_db, history_ids)


    @classmethod
    async def export_history_list(cls, query_db: AsyncSession, query_object: HistoryPageModel, data_scope_sql) -> bytes:
        history_list = await HistoryDao.get_history_list(query_db, query_object, data_scope_sql, is_page=False)
        filed_list = await SysTableService.get_sys_table_list(query_db, SysTablePageModel(tableName='history'), is_page=False)
        filtered_filed = sorted(filter(lambda x: x["show"] == '1', filed_list), key=lambda x: x["sequence"])
        new_data = []
        for item in history_list:
            mapping_dict = {}
            for fild in filtered_filed:
                if fild["prop"] in item:
                    mapping_dict[fild["label"]] = item[fild["prop"]]
            new_data.append(mapping_dict)
        binary_data = export_list2excel(new_data)
        return binary_data