# -*- coding:utf-8 -*-
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import List, Literal, Optional, Union
from module_admin.annotation.pydantic_annotation import as_query


class HistoryModel(BaseModel):
    """
    表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)
    create_by: Optional[str] =  Field(default=None, description='创建者')
    create_time: Optional[datetime] =  Field(default=None, description='创建时间')
    del_flag: Optional[str] =  Field(default=None, description='删除标志（0代表存在 2代表删除）')
    dept_id: Optional[int] =  Field(default=None, description='部门id')
    id: Optional[int] =  Field(default=None, description='图像ID')
    image: Optional[str] =  Field(default=None, description='图像')
    lat: Optional[float] =  Field(default=None, description='纬度')
    lng: Optional[float] =  Field(default=None, description='经度')
    location: Optional[str] =  Field(default=None, description='地点')
    predclass: Optional[str] =  Field(default=None, description='预测类别')
    predlabel: Optional[str] =  Field(default=None, description='预测标签')
    predscore: Optional[float] =  Field(default=None, description='预测分数')
    reportid: Optional[int] =  Field(default=None, description='上报ID')
    time: Optional[str] =  Field(default=None, description='时间')
    update_by: Optional[str] =  Field(default=None, description='更新者')
    update_time: Optional[datetime] =  Field(default=None, description='更新时间')


@as_query
class HistoryPageModel(HistoryModel):
    """
    分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')