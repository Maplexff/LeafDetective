# -*- coding:utf-8 -*-

from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from typing import List
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.entity.vo.import_vo import ImportModel
from module_admin.service.import_service import ImportService
from module_admin.service.login_service import LoginService
from module_admin.aspect.data_scope import GetDataScope
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.annotation.log_annotation import Log
from utils.response_util import ResponseUtil
from utils.common_util import bytes2file_response

from module_history.entity.vo.history_vo import HistoryPageModel, HistoryModel
from module_history.service.history_service import HistoryService

historyController = APIRouter(prefix='/history/history', dependencies=[Depends(LoginService.get_current_user)])


@historyController.get('/list', dependencies=[Depends(CheckUserInterfaceAuth('history:history:list'))])
async def get_history_list(
        request: Request,
        query_db: AsyncSession = Depends(get_db),
        page_query: HistoryPageModel = Depends( HistoryPageModel.as_query),
        data_scope_sql: str = Depends(GetDataScope('History'))
):
    history_result = await HistoryService.get_history_list(query_db, page_query, data_scope_sql)

    return ResponseUtil.success(model_content=history_result)

@historyController.get('/getById/{historyId}', dependencies=[Depends(CheckUserInterfaceAuth('history:history:list'))])
async def get_history_by_id(
        request: Request,
        historyId: int,
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('History'))
):
    history = await HistoryService.get_history_by_id(query_db, historyId)
    return ResponseUtil.success(data=history)


@historyController.post('/add', dependencies=[Depends(CheckUserInterfaceAuth('history:history:add'))])
@Log(title='history', business_type=BusinessType.INSERT)
async def add_history (
    request: Request,
    add_model: HistoryModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):

    add_model.create_by = current_user.user.user_id
    add_model.dept_id = current_user.user.dept_id
    add_dict_type_result = await HistoryService.add_history(query_db, add_model)
    return ResponseUtil.success(data=add_dict_type_result)

@historyController.put('/update', dependencies=[Depends(CheckUserInterfaceAuth('history:history:edit'))])
@Log(title='history', business_type=BusinessType.UPDATE)
async def update_history(
    request: Request,
    edit_model: HistoryModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_dict_type_result = await HistoryService.update_history(query_db, edit_model)
    return ResponseUtil.success(data=add_dict_type_result)


@historyController.delete('/delete/{historyIds}', dependencies=[Depends(CheckUserInterfaceAuth('history:history:del'))])
@Log(title='history', business_type=BusinessType.DELETE)
async def del_history(
    request: Request,
    historyIds: str,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    ids = historyIds.split(',')
    del_result = await HistoryService.del_history(query_db, ids)
    return ResponseUtil.success(data=del_result)

@historyController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('history:history:export'))])
@Log(title='history', business_type=BusinessType.EXPORT)
async def export_history(
    request: Request,
    history_form: HistoryPageModel = Form(),
    query_db: AsyncSession = Depends(get_db),
    data_scope_sql: str = Depends(GetDataScope('History')),
):
    # 获取全量数据
    export_result = await HistoryService.export_history_list(
        query_db, history_form, data_scope_sql
    )
    return ResponseUtil.streaming(data=bytes2file_response(export_result))

@historyController.post('/import', dependencies=[Depends(CheckUserInterfaceAuth('history:history:import'))])
async def import_history(request: Request,
                      import_model: ImportModel,
                      query_db: AsyncSession = Depends(get_db),
                      current_user: CurrentUserModel = Depends(LoginService.get_current_user)
    ):
    """
    导入数据
    """
    await ImportService.import_data(query_db, import_model, current_user)
    return ResponseUtil.success()